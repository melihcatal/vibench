import os
from azure.cognitiveservices.language.text.analytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

def stored_asset_summary(text):
    subscription_key = os.getenv('TEXT_ANALYTICS_SUBSCRIPTION_KEY')
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    text_analytics_client = TextAnalyticsClient(endpoint, CognitiveServicesCredentials(subscription_key))
    result = text_analytics_client.summarize(documents=[{'id': '1', 'text': text}])
    print(f'Summary: {result[0].summary_text}')
    return result[0].summary_text