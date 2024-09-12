from bobik_tools.tools import tool_node, tools
from django.conf import settings
from django.db import models
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import tools_condition
from psycopg import Connection
from psycopg.rows import dict_row


class AutoCleanupPostgresSaver(PostgresSaver):
    def __del__(self):
        if not self.conn.closed:
            self.conn.close()


class Checkpoints(models.Model):
    thread_id = models.TextField()
    checkpoint_ns = models.TextField()
    checkpoint_id = models.TextField(primary_key=True)
    parent_checkpoint_id = models.TextField()
    type = models.TextField()
    checkpoint = models.JSONField()
    metadata = models.JSONField()

    class Meta:
        managed = False
        db_table = "checkpoints"


# Create your models here.
class BobikSite(models.Model):
    site = models.OneToOneField("sites.Site", on_delete=models.CASCADE)

    ai_model = models.CharField(max_length=30, default="claude-3-5-sonnet-20240620")
    ai_api_key = models.CharField(max_length=255)

    admin_email = models.EmailField(
        max_length=255,
        help_text="E-mail na który będą wysyłane ankiety preanestetyczne",
    )
    admin_password = models.CharField(
        max_length=50, help_text="Poczatkowe hasło administratora"
    )

    checkpointer = None
    graph = None

    def get_model(self):
        if self.ai_model.startswith("gpt-"):
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(
                model=self.ai_model, api_key=self.ai_api_key, temperature=0.0
            )
        elif self.ai_model.startswith("claude-"):
            from langchain_anthropic import ChatAnthropic

            llm = ChatAnthropic(
                model=self.ai_model, api_key=self.ai_api_key, temperature=0.0
            )
        else:
            raise NotImplementedError(
                f"Model {self.ai_model} is supported by bobik-online"
            )
        return llm

    def get_model_with_tools(self):
        return self.get_model().bind_tools(tools)

    def get_graph_builder(self):
        graph_builder = StateGraph(MessagesState)

        def chatbot(state: MessagesState):
            return {"messages": [self.get_model_with_tools().invoke(state["messages"])]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("tools", tool_node)

        graph_builder.set_entry_point("chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)

        return graph_builder

    def get_graph(self):
        if not self.graph:
            self.graph = self.get_graph_builder().compile(
                checkpointer=self.get_checkpointer()
            )
        return self.graph

    def get_checkpointer(self):
        # Podłącz checkpointer do takiego samego backendu db jak Djagno

        # from psycopg.rows import dict_row
        #
        # self._db_conn = Connection.connect(
        #     self.db_url, autocommit=True, prepare_threshold=0, row_factory=dict_row
        # )

        if not self.checkpointer:
            # TODO: dobrze by było zmienic system serializacji na taki sam, jakiego uzywa Django.
            # Ewentualnie nawet otworzyc drugie połączenie do bazy danych korzystając z tych
            # samych ustawień.
            # Na ten moment LangChain nie ma Checkpointera dla Django.
            if (
                settings.DATABASES["default"]["ENGINE"]
                != "django.db.backends.postgresql"
            ):
                raise NotImplementedError(
                    "Checkpointer wspiera wyłącznie PostgreSQL..."
                )

            s = settings.DATABASES["default"]
            host = s.get("HOST") or "localhost"
            user = s.get("USER") or "postgres"
            db = s.get("NAME") or user
            #
            self._db_url = f"postgres://{user}@{host}/{db}"
            self._db_conn = Connection.connect(
                self._db_url, autocommit=True, prepare_threshold=0, row_factory=dict_row
            )
            self.checkpointer = AutoCleanupPostgresSaver(self._db_conn)
            self.checkpointer.setup()

        return self.checkpointer

    def send_message(self, config, msg):
        return list(
            self.get_graph().stream({"messages": [msg]}, config, stream_mode="values")
        )

    def send_system_message(
        self, config, msg, human_message="Przeprowadź wywiad z pacjentem"
    ):
        return list(
            self.get_graph().stream(
                {"messages": [SystemMessage(msg), HumanMessage(human_message)]},
                config,
                stream_mode="values",
            )
        )

    def send_user_message(self, config, msg):
        return self.send_message(config, HumanMessage(msg))

    def get_messages(self, config):
        return self.get_checkpointer().list(config=config)
