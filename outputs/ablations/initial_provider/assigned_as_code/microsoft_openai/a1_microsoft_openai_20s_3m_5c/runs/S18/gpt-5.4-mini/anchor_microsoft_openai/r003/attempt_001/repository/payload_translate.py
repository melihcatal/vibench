from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_payload(text, target_language, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    response = client.translate(content=[text], to=[target_language])
    translated = response[0].translations[0].text if response and response[0].translations else text
    return {'translated_text': translated}
