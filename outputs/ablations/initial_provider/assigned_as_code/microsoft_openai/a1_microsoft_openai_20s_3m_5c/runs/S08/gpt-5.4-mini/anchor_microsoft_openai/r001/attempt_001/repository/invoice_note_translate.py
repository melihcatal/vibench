from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def invoice_note_translate(payload, config=None):
    config = config or {}
    with TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key'])) as client:
        result = client.translate(content=payload.get('text', ''), to=[config.get('target_language', 'en')])
    translations = []
    for item in result:
        for translation in item.translations:
            translations.append({'language': translation.to, 'text': translation.text})
    return {'translations': translations}
