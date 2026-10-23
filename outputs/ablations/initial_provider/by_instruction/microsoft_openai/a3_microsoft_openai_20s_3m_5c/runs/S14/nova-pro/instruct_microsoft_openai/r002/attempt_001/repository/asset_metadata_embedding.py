import os
from azure.cognitiveservices.language.text.analytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

def asset_metadata_embedding(text):
    subscription_key = os.getenv('TEXT_ANALYTICS_SUBSCRIPTION_KEY')
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    text_analytics_client = TextAnalyticsClient(endpoint, CognitiveServicesCredentials(subscription_key))
    result = text_analytics_client.extract_key_phrases(documents=[{'id': '1', 'text': text}])
    print(f'Key phrases: {result[0].key_phrases}')
    return result[0].key_phrases