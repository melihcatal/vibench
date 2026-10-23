import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

text_analytics_client = TextAnalyticsClient(endpoint=f'https://{os.environ.get('AZURE_TEXT_ANALYTICS_REGION')}.api.cognitive.microsoft.com/', credential=TextAnalyticsApiKeyCredential(os.environ.get('AZURE_TEXT_ANALYTICS_KEY')))

def transcript_embedding(text):
    result = text_analytics_client.extract_key_phrases(text)
    return result[0].key_phrases