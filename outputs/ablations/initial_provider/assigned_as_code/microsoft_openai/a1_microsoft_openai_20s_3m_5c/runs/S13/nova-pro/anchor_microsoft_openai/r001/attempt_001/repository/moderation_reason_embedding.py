from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def moderation_reason_embedding(payload, config=None):
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    result = client.extract_key_phrases(documents=[payload['text']])
    return {'embedding': result[0].key_phrases}