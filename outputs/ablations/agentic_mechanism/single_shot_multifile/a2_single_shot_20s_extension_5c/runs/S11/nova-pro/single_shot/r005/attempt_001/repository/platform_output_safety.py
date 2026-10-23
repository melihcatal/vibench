import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import Screen, TextScreen
from azure.core.credentials import AzureKeyCredential

def check_platform_output_safety(text):
    endpoint = os.getenv('CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('CONTENT_SAFETY_KEY')
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    screen = Screen(text=TextScreen(content=text))
    result = client.screen(screen)
    return result