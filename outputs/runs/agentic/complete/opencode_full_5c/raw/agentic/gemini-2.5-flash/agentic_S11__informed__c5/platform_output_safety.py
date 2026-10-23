import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def check_platform_output_safety(text_output: str) -> dict:
    """Checks platform model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_output,
        categories=[
            TextCategory.HATE,
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
        ],
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate": response.categories_analysis[0].severity
        if response.categories_analysis
        else None,
        "violence": response.categories_analysis[1].severity
        if response.categories_analysis
        else None,
        "self_harm": response.categories_analysis[2].severity
        if response.categories_analysis
        else None,
        "sexual": response.categories_analysis[3].severity
        if response.categories_analysis
        else None,
    }
    return safety_results
