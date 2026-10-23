import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def safety_threshold(text: str, thresholds: dict) -> bool:
    """
    Applies category thresholds to decide whether to allow text based on Azure AI Content Safety analysis.
    `thresholds` is a dictionary where keys are category names (e.g., 'Hate', 'SelfHarm') and values are the max allowed severity.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    allowed = True
    for category in response.categories:
        category_name = category.category.value
        severity = category.severity

        if category_name in thresholds:
            if severity >= thresholds[category_name]:
                allowed = False
                break
    return allowed

