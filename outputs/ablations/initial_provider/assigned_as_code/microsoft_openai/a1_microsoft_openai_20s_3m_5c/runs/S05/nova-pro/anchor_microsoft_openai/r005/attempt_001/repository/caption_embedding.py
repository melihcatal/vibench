import os
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential


def embed_caption(text):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_API_KEY')
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = text_analytics_client.analyze_sentiment(documents=[text])[0]
    return result.sentiment_score