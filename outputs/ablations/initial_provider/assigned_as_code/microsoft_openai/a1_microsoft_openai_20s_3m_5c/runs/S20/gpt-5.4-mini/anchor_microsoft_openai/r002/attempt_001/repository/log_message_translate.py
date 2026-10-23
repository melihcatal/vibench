from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def log_message_translate(payload, config=None):
    client = TextTranslationClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    result = client.translate(content=[payload['text']], to=[payload['target_language']])
    return {'translated_text': result[0].translations[0].text}
