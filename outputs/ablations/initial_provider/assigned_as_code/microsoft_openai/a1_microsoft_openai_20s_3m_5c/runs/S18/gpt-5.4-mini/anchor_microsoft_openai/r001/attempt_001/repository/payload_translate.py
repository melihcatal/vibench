from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_payload_text(text, target_language, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['translation_endpoint'], credential=AzureKeyCredential(config['translation_key']))
    result = client.translate(content=[text], to=[target_language])
    return {'translated_text': result[0].translations[0].text}
