from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def stored_text_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translator_endpoint'], credential=AzureKeyCredential(config['translator_key']))
    result = client.translate(content=[payload['text']], to=[payload['target_language']])
    return {'translated_text': result[0].translations[0].text}
