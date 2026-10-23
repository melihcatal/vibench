import os
from azure.ai.contentsafety import ContentSafetyClient, AzureKeyCredential
from azure.ai.contentsafety.models import TextScreen


def moderate_transcript(transcript):
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    screen = TextScreen(text=transcript)
    result = client.classify_text(screen)
    return result.result.categories[0].severity
