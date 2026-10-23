from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def alt_text_translate(payload, config=None):
    config = dict(config or {})
    endpoint = config['endpoint']
    key = config['api_key']
    target_language = config.get('target_language', 'es')
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    text = payload.get('text', '')
    response = client.translate(content=[text], to=[target_language])
    translated = response[0].translations[0].text if response and response[0].translations else text
    return {'translated_text': translated}
