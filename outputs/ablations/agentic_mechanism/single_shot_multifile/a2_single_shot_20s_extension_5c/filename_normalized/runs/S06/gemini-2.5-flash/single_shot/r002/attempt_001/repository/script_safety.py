import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_script_safety(text: str) -> dict:
    """
    Checks the narration script for unsafe content using Azure Content Safety.
    Returns a dictionary of safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Supported categories for analysis: Hate, SelfHarm, Sexual, Violence
    # You can specify thresholds for each category if needed
    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )

    response = client.analyze_text(request)

    safety_results = {}
    for category in response.categories_analysis:
        safety_results[category.category.value] = {
            "severity": category.severity, # 0-7, 0 means no risk
            "category": category.category.value
        }
    return safety_results
