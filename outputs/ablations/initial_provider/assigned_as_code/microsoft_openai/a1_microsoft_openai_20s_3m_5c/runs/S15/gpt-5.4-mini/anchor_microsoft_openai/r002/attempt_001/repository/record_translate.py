from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def record_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translator_endpoint'], credential=AzureKeyCredential(config['translator_key']))
    response = client.translate(content=[payload['text']], to=[payload['target_language']])
    translated = response[0].translations[0].text if response and response[0].translations else payload['text']
    return {'translated_text': translated}
