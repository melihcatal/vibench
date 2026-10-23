import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory, TextModerationOptions


def check_vendor_text_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    options = TextModerationOptions(text=text, categories=[TextCategory.TOXICITY])
    response = client.analyze_text(options)
    severity = (
        response.toxicity.severity.value
        if hasattr(response.toxicity, "severity") and response.toxicity.severity
        else "none"
    )
    return {
        "safe": severity in ["none", "low"],
        "severity": severity,
        "category": "toxicity",
    }
