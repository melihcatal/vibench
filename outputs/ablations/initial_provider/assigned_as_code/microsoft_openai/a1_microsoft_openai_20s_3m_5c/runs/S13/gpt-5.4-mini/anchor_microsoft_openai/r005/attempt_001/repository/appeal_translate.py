from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from safety_client import load_safety_config


def appeal_translate(payload, config=None):
    config = load_safety_config(config)
    text = (payload or {}).get('text', '')
    target_language = (payload or {}).get('target_language', 'en')
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    response = client.translate(content=[text], to=[target_language])
    translated = response[0].translations[0].text if response and response[0].translations else text
    return {'text': translated, 'language': target_language}
