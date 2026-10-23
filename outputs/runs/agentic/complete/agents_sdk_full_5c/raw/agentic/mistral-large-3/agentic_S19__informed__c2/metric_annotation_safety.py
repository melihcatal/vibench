from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextCategory, AnalyzeTextOptions
import os


def check_metric_annotation_safety(text: str) -> bool:
    """Check free-text metric labels or annotations for unsafe text using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    return all(
        result.severity <= 2 for result in response.categories_analysis
    )