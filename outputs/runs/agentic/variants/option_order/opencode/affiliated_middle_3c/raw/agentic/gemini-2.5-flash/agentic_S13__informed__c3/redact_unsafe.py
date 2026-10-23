import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import ModerationResult


def redact_unsafe(text: str, threshold_severity: int = 2) -> str:
    client = ContentSafetyClient(
        os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
        AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
    )
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    for category_result in response.categories_analysis:
        if category_result.severity >= threshold_severity:
            return "[REDACTED]"
    return text
