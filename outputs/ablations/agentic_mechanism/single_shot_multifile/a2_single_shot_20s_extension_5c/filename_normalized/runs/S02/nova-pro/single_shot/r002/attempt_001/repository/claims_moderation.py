import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def moderate_claims(text):
    endpoint = os.environ['AZURE_TEXT_ANALYTICS_ENDPOINT']
    credential = TextAnalyticsApiKeyCredential(os.environ['AZURE_TEXT_ANALYTICS_KEY'])
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.analyze_sentiment(documents=[text])[0]
    if result.sentiment == 'negative':
        return 'Moderated'
    return 'Approved'