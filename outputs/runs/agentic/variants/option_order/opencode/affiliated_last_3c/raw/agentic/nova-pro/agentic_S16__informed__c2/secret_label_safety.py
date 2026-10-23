import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextScreen
from azure.core.credentials import AzureKeyCredential


# Check secret labels and notes for unsafe text
def secret_label_safety(text):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    screen = TextScreen(text=text)
    result = client.text_screen(screen)
    return result
