FROM python:3.12-bookworm

RUN pip install poetry

COPY . .

RUN chmod 755 ./appserver-entrypoint.sh

RUN poetry install

ENTRYPOINT ["./appserver-entrypoint.sh"]