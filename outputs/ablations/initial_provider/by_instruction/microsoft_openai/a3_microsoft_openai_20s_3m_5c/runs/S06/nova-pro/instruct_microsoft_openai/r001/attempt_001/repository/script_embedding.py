import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def embed_script(script: str) -> str:
    subscription_key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    credential = TextAnalyticsApiKeyCredential(subscription_key)
    client = TextAnalyticsClient(endpoint, credential)
    result = client.extract_key_phrases(script)
    return ' '.join(result.key_phrases)