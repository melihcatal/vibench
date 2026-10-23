import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

client = DocumentTranslationClient(
    endpoint=os.getenv("TRANSLATION_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("TRANSLATION_KEY")),
)


def translate_text(text, target_language="es"):
    result = client.translate(text, target_language)
    return result.translations[0].text
