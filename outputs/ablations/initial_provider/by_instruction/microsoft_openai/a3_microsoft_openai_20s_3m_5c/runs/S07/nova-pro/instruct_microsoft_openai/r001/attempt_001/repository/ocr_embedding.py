import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics.models import TextDocumentInput

def embed_text(text):
    client = TextAnalyticsClient(endpoint=os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT'), credential=os.getenv('AZURE_TEXT_ANALYTICS_KEY'))
    document = TextDocumentInput(id='1', text=text)
    result = client.extract_key_phrases([document])[0]
    return result.key_phrases