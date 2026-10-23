import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_batch(texts):
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    )
    results = []
    for text in texts:
        options = AnalyzeTextOptions(text=text)
        result = client.analyze_text(options)
        results.append(result)
    return results
