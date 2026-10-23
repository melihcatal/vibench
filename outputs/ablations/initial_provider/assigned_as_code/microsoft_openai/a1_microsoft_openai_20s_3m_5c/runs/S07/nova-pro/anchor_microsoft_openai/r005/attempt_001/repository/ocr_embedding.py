import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def embed_text(text):
    config = {
        'endpoint': os.getenv('TEXT_ANALYTICS_ENDPOINT'),
        'api_key': os.getenv('TEXT_ANALYTICS_API_KEY')
    }
    with TextAnalyticsClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.extract_key_phrases(text)
    return {'embeddings': result.content}