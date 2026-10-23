import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


def check_safety(text: str):
    """
    Checks prompts and generated text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get(
        "AZURE_CONTENT_SAFETY_ENDPOINT"
    )  # Provider-specific environment variable
    key = os.environ.get(
        "AZURE_CONTENT_SAFETY_KEY"
    )  # Provider-specific environment variable

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    safety_results = {
        "Hate": response.hate_result.severity,
        "SelfHarm": response.self_harm_result.severity,
        "Sexual": response.sexual_result.severity,
        "Violence": response.violence_result.severity,
    }
    return safety_results
