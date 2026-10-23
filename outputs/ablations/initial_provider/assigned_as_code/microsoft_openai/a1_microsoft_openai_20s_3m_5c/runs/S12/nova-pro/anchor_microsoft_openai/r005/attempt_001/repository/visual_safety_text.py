from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def check_visual_labels_for_unsafe_text(text, config=None):
    config = config or {}
    with TextAnalyticsClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.detect_language(text)
        language = result[0].primary_language.name
        result = client.analyze_sentiment([text])
        sentiment_score = result[0].sentiment
        return {'language': language, 'sentiment_score': sentiment_score}