from typing import List

from bobik_prompts.models import BobikPrompt
from django.core.mail import send_mail
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


@tool
def wygeneruj_liste_badan(
    wiek_pacjenta: int,
    plec_pacjenta: str,
    jezyk_pacjenta: str,
    rodzaj_zabiegu: str,
    tryb_zabiegu: str,
    uczulenia_pacjenta: List[str],
    stosowane_leki: List[str],
    obecne_choroby: List[str],
    przebyte_choroby: List[str],
    przebyte_operacje: List[str],
    naduzywane_substancje: List[str],
    wzrost_pacjenta: int,
    waga_pacjenta: int,
):
    """Generuje liste badan dla pacjenta o okreslonym wieku do okreslonej operacji"""

    from bobik_setup.models import BobikSite

    model = BobikSite.objects.get(site_id=1).get_model()

    system_message = BobikPrompt.objects.get(
        pk=BobikPrompt.PromptType.BADANIA_PRZED_OPERACJA
    ).tresc

    prompt = f"""
    Dane pacjenta: wiek {wiek_pacjenta}, płeć {plec_pacjenta}.
    Lista uczuleń pacjenta: {uczulenia_pacjenta}.
    Lista leków stosowanych przez pacjenta: {stosowane_leki}.
    Lista obecnych chorób pacjenta: {obecne_choroby}
    Lista przebytych chorób pacjenta: {przebyte_choroby}.
    Lista przebytych operacji przez pacjenta: {przebyte_operacje}
    Lista nadużywanych przez pacjenta substancji: {naduzywane_substancje}

    Pacjent przygotowywany jest do zabiegu: {rodzaj_zabiegu}.
    Tryb zabiegu: {tryb_zabiegu}.

    Użyj języka: {jezyk_pacjenta}.

    Waga pacjenta: {waga_pacjenta}.
    Wzrost pacjenta: {wzrost_pacjenta}.
    """

    messages = [
        ("system", system_message),
        ("human", prompt),
    ]

    ret = model.invoke(messages)
    print("X" * 90)
    print(ret)
    return ret.content


@tool
def send_email(subject: str, body_text: str, recipient_list: List[str]):
    """Call to send an e-mail with the log"""
    # print(f"send_email called, {subject=} {body_text=} {recipient_list=}")
    send_mail(
        subject=subject,
        message=body_text,
        from_email=None,
        recipient_list=recipient_list,
    )
    return f"E-mail został wysłany. Dziękujemy za współpracę. "


tools = [send_email, wygeneruj_liste_badan]

tool_node = ToolNode(tools)
