from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def log_embedding(log_text, config):
    credential = AzureKeyCredential(config['text_analytics_key'])
    client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=credential)
    result = client.extract_key_phrases(documents=[log_text])[0]
    return result.key_phrases