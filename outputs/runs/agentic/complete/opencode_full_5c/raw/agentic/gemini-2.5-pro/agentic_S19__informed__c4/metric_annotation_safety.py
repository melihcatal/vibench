import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_annotation_safety(text_to_check: str) -> dict:
    """
    Checks free-text annotations for safety using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_check,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.message}"}

    results = {}
    if response.hate_result:
        results["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        results["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        results["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        results["violence"] = {"severity": response.violence_result.severity}

    return results
