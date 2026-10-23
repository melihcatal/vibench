from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def record_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    text = payload.get('text') or payload.get('content') or ''
    target_language = payload.get('target_language', 'en')
    translated = client.translate(content=[text], to=[target_language])
    return translated[0] if translated else None
