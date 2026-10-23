import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_annotation_safety(text: str):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.HATE,
        ],
    )

    response = client.analyze_text(request)

    results = {}
    for category in response.categories_analysis:
        results[category.category.value] = {
            "severity": category.severity,
            "detected": category.severity > 0,  # Assuming severity > 0 means detected
        }
    return results
