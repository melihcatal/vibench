from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def dashboard_note_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    response = client.translate(content=[payload['text']], to=[payload['target_locale']])
    return {'text': response[0].translations[0].text}
