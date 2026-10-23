from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential
from azure.core.credentials import AzureKeyCredential

def get_embedding(text):
    endpoint = 'https://<YOUR_TEXT_ANALYTICS_ENDPOINT>.cognitiveservices.azure.com/'
    key = 'YOUR_TEXT_ANALYTICS_KEY'
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = text_analytics_client.extract_key_phrases(documents=[text])
    return result[0].key_phrases