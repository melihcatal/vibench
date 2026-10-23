import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def check_safety(text):
    config = {
        'endpoint': os.getenv('CONTENT_SAFETY_ENDPOINT'),
        'api_key': os.getenv('CONTENT_SAFETY_API_KEY')
    }
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.classify_text(text)
    return {'safety_result': result.content}