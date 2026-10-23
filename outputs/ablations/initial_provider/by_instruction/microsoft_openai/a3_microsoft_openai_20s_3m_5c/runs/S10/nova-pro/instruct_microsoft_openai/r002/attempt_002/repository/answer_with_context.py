import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def answer_with_context(question, context):
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    key = os.getenv('AZURE_OPENAI_KEY')
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.answer_question(question=question, context=context)
    return result.answers[0].text