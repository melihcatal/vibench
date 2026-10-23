import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions


def safety_threshold(text, threshold):
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    )
    options = AnalyzeTextOptions(text=text)
    result = client.analyze_text(options)
    for category in result.categories:
        if category.severity >= threshold:
            return False
    return True
