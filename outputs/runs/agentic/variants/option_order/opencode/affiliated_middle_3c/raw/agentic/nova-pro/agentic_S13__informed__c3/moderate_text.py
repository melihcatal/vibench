import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_text(text):
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    )
    options = AnalyzeTextOptions(text=text)
    result = client.analyze_text(options)
    return result
