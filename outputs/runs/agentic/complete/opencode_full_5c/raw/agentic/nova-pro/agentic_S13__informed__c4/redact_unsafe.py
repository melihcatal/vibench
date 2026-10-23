import os

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
)


def redact_unsafe(text):
    options = AnalyzeTextOptions(text=text)
    result = client.analyze_text(options)
    redacted_text = text
    for category in result.categories:
        if category.severity > 0:
            redacted_text = redacted_text.replace(category.text, "[REDACTED]")
    return redacted_text
