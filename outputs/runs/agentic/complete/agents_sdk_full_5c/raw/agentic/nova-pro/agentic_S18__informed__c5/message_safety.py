import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyApiKeyCredential
from azure.ai.contentsafety.models import TextScreen

# Configuration
endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
key = os.getenv('AZURE_CONTENT_SAFETY_KEY')

# Authenticate
client = ContentSafetyClient(endpoint=endpoint, credential=ContentSafetyApiKeyCredential(key))

# Check text safety
def check_text_safety(text):
    result = client.text_screen(TextScreen(text=text))
    return result