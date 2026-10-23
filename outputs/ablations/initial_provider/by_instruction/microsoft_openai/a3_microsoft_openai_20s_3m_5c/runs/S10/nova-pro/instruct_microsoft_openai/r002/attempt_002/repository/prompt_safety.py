import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def check_prompt_safety(prompt):
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    key = os.getenv('AZURE_OPENAI_KEY')
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.analyze_sentiment(documents=[prompt])[0]
    return result.sentiment