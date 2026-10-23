import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyKeyCredential
from azure.ai.contentsafety.models import Screen

content_safety_client = ContentSafetyClient(endpoint=os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=ContentSafetyKeyCredential(os.environ.get('AZURE_CONTENT_SAFETY_KEY')))

def moderate_transcript(text):
    screen = Screen(text=text)
    result = content_safety_client.screen_text(screen)
    return result