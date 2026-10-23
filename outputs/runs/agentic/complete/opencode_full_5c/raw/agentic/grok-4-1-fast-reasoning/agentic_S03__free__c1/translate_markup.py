import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient


def translate_markup(markup: str, source_lang: str, target_lang: str) -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = "https://api.cognitive.microsofttranslator.com"
    credential = AzureKeyCredential(key)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)
    poller = client.submit_translation(
        contents=[markup],
        content_type="text/html",
        target_languages=[target_lang],
        source_language=source_lang,
    )
    results = poller.result()
    return results[0].translations[0].text
