from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentAction
from azure.core.credentials import AzureKeyCredential


def check_message_safety(text, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    result = client.analyze([text], actions=[AnalyzeSentimentAction()])
    status = 'unsafe' if any(doc.confidence_scores.negative > 0.7 for doc in result) else 'safe'
    return {'status': status}
