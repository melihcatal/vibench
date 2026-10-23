from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def log_message_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    text = str(payload.get('text', ''))
    target_language = payload.get('target_language', 'es')
    result = client.translate(content=[text], to=[target_language])
    translated = result[0].translations[0].text if result and result[0].translations else ''
    return {'text': translated, 'target_language': target_language}
