import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions


def redact_unsafe(text):
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    )
    options = AnalyzeTextOptions(text=text)
    result = client.analyze_text(options)
    redacted_text = text
    for category in result.categories:
        if category.severity > 0:
            redacted_text = redacted_text.replace(
                category.text, "*" * len(category.text)
            )
    return redacted_text
