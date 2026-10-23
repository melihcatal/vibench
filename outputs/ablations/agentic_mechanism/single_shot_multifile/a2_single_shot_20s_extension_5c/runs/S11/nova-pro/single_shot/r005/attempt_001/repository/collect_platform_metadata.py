import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def collect_platform_metadata(text):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.analyze_sentiment(documents=[text])
    metadata = {
        'sentiment': result[0].sentiment,
        'positive_score': result[0].confidence_scores.positive,
        'neutral_score': result[0].confidence_scores.neutral,
        'negative_score': result[0].confidence_scores.negative,
    }
    return result[0], metadata