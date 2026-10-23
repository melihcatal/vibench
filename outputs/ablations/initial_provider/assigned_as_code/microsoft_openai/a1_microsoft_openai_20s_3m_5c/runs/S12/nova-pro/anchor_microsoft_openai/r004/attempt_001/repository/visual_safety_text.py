from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def visual_safety_text(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    result = client.detect_language(payload['labels'])
    is_safe = all([not label['name'].lower() in config.get('unsafe_keywords', []) for label in result])
    return {'is_safe': is_safe}