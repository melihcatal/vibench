import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_profile_text(text: str) -> dict:
    """
    Moderates user profile text using Azure AI Content Safety.
    Returns a dictionary indicating if the text is safe and severity levels.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(
            f"Analyze text failed. Error code: {e.error.code}, Error message: {e.error.message}"
        )
        raise

    results = {}
    for category in response.categories_analysis:
        results[category.category.value] = category.severity

    # Simplified safety check: any severity > 0 is considered not safe
    is_safe = all(sev == 0 for sev in results.values())

    return {"is_safe": is_safe, "severity_levels": results}
