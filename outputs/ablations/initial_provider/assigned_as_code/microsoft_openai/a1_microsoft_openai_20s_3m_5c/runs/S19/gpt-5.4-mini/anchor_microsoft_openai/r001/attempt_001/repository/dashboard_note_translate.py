from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def dashboard_note_translate(payload, config=None):
    config = dict(config or {})
    client = TextTranslationClient(endpoint=config['translator_endpoint'], credential=AzureKeyCredential(config['translator_key']))
    target_language = payload['target_language']
    source_text = payload['text']
    result = client.translate(content=[source_text], to=[target_language])
    translated = result[0].translations[0].text if result and result[0].translations else source_text
    return {'text': translated, 'language': target_language}
