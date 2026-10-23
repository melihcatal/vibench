import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyCredential

client = ContentSafetyClient(credential=ContentSafetyCredential(os.getenv('AZURE_CONTENT_SAFETY_KEY')), endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'))

def check_safety(text):
    result = client.text_moderation(text)
    return result.results[0].category1.score