import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_text(text, target_language):
    config = {
        'endpoint': os.getenv('TRANSLATION_ENDPOINT'),
        'api_key': os.getenv('TRANSLATION_API_KEY')
    }
    with DocumentTranslationClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.translate_document(text, target_language)
    return {'translated_text': result.content}