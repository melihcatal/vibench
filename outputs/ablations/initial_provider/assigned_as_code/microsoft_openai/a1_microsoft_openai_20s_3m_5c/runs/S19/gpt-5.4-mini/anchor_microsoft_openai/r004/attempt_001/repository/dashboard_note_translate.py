from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def dashboard_note_translate(payload, config=None):
    config = config or {}
    text = payload.get('text') or payload.get('note') or ''
    target_language = payload.get('target_language') or config.get('target_language', 'en')
    endpoint = config.get('translator_endpoint')
    key = config.get('translator_key')
    if endpoint and key:
        with TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key)) as client:
            response = client.translate(content=[text], to=[target_language])
        translated = response[0].translations[0].text if response else text
    else:
        translated = text
    return {'source_text': text, 'target_language': target_language, 'translated_text': translated}
