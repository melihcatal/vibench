import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_annotation_safety(text_annotation: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

    Args:
        text_annotation: The text content to analyze.

    Returns:
        A dictionary with the safety analysis result.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError as e:
        raise ValueError(f"Environment variable {e} is not set.") from e

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_annotation,
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
        return {"error": f"HTTP response error: {e.message}"}

    results = {
        "is_safe": True,
        "categories": {}
    }

    for category in response.categories_analysis:
        results["categories"][category.category.value] = {
            "severity": category.severity
        }
        if category.severity > 0:
            results["is_safe"] = False

    return results
