from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def audit_summary(payload, config=None):
    client = TextAnalyticsClient(
        endpoint=config['endpoint'],
        credential=AzureKeyCredential(config['api_key']),
    )
    docs = [payload.get('summary', '')]
    result = client.analyze_sentiment(docs)[0]
    return {'provider': 'azure-ai-textanalytics', 'sentiment': result.sentiment, 'score': result.confidence_scores.positive}
