import os

from azure.ai.translation.text import TranslatorClient
from azure.core.credentials import AzureKeyCredential

# [LATER-STEP] dashboard_note_translate.py


def translate_dashboard_note(text, to_language):
    credential = AzureKeyCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TranslatorClient(
        endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"), credential=credential
    )
    result = client.translate(content=[text], to=to_language)
    return result[0].translations[0].text
