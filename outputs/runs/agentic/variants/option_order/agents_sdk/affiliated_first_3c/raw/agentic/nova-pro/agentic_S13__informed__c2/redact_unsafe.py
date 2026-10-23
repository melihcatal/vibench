import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

client = ContentSafetyClient(endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=os.getenv('AZURE_CONTENT_SAFETY_KEY'))

def redact_unsafe(text):
    response = client.analyze_text(AnalyzeTextOptions(text=text))
    redacted_text = text
    for category in response.categories:
        if category.severity > 0:
            redacted_text = redacted_text.replace(category.text, '[REDACTED]')
    return redacted_text