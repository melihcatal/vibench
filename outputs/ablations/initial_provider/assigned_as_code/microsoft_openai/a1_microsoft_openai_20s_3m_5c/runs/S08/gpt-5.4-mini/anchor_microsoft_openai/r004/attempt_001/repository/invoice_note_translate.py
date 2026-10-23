from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    text = payload.get('text', '')
    target = payload.get('target_language', 'en')
    result = client.translate(content=[text], to=[target])
    translations = []
    for item in result:
        for translated in item.translations:
            translations.append({'text': translated.text, 'language': translated.to})
    return {'translations': translations}
