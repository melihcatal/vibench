import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

client = ContentSafetyClient(endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=os.getenv('AZURE_CONTENT_SAFETY_KEY'))

def safety_threshold(text, threshold=0.5):
    response = client.analyze_text(AnalyzeTextOptions(text=text))
    for category in response.categories:
        if category.severity > threshold:
            return False
    return True