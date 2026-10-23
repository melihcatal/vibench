import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient


def translate_dictionary_values(
    d: dict[str, str], source_lang: str, target_lang: str
) -> dict[str, str]:
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    credential = AzureKeyCredential(key)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)
    values = list(d.values())
    poller = client.submit_batch_translation(
        body=values, source_language=source_lang, target_language=target_lang
    )
    results = poller.wait_for_completion_and_get_result()
    translated_texts = [r.text for r in results]
    return dict(zip(d.keys(), translated_texts))
