from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from storage_models import extract_text_payload


def stored_text_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translator_endpoint'], credential=AzureKeyCredential(config['translator_key']))
    source_text = extract_text_payload(payload.get('text') or payload.get('content'))
    response = client.translate(content=[source_text], to=[payload['target_language']], from_parameter=payload.get('source_language'))
    translated = response[0].translations[0].text if response and response[0].translations else ''
    return {'translated_text': translated}
