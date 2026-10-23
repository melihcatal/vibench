import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

client = ContentSafetyClient(endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=os.getenv('AZURE_CONTENT_SAFETY_KEY'))

def moderate_batch(texts):
    results = []
    for text in texts:
        response = client.analyze_text(AnalyzeTextOptions(text=text))
        results.append(response)
    return results