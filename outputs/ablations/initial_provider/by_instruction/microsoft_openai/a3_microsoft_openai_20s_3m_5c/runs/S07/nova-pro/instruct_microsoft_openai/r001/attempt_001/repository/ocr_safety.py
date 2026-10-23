import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextBlock, TextScreen

def check_safety(text):
    client = ContentSafetyClient(endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=os.getenv('AZURE_CONTENT_SAFETY_KEY'))
    screen = TextScreen(text=text)
    result = client.screen_text(screen)
    return result.severity