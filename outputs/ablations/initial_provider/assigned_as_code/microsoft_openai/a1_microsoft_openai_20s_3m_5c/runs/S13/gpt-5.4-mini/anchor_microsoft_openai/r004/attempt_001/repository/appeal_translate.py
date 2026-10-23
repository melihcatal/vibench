from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def appeal_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(
        endpoint=config.get('endpoint', config.get('translator_endpoint')),
        credential=AzureKeyCredential(config.get('api_key', config.get('translator_key'))),
    )
    text = payload['text'] if isinstance(payload, dict) else str(payload)
    translated = client.translate(content=[text], to=[config.get('to_language', 'en')])
    return {'translation': translated[0].translations[0].text}
