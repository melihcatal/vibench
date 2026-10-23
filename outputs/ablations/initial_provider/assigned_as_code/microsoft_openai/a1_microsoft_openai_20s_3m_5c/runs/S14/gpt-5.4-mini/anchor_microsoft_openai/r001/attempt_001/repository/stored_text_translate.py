from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def stored_text_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translator_endpoint'], credential=AzureKeyCredential(config['translator_key']))
    response = client.translate(content=[payload['text']], to=[payload['target_language']], from_parameter=payload.get('source_language'))
    return {'translations': [{'text': item.translations[0].text, 'language': item.translations[0].to} for item in response]}
