import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_unsafe_copy(text: str) -> dict:
    """Checks localized copy for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    # Default thresholds for all categories as per Azure AI Content Safety documentation
    # violence_threshold=2, hate_threshold=2, sexual_threshold=2, self_harm_threshold=2

    response = client.analyze_text(request)

    # Convert response to a dictionary for easier consumption
    result = {
        "hate": {"severity": response.hate_result.severity, "category": str(response.hate_result.category)},
        "sexual": {"severity": response.sexual_result.severity, "category": str(response.sexual_result.category)},
        "self_harm": {"severity": response.self_harm_result.severity, "category": str(response.self_harm_result.category)},
        "violence": {"severity": response.violence_result.severity, "category": str(response.violence_result.category)},
    }

    return result
