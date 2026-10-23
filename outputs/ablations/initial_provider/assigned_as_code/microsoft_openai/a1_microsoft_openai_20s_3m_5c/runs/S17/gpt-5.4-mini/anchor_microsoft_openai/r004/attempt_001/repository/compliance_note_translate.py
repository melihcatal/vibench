from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def compliance_note_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translation_endpoint'], credential=AzureKeyCredential(config['translation_key']))
    target = payload.get('target_language', 'en')
    response = client.translate(content=[payload.get('text', '')], to=[target])
    translated = response[0].translations[0].text if response and response[0].translations else ''
    return {'translated_text': translated, 'target_language': target, 'provider': 'azure-ai-translation-text'}
