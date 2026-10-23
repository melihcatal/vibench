import os
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential


def summarize_text(text):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_API_KEY')
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = text_analytics_client.extract_key_phrases(documents=[text])[0]
    return result.key_phrases