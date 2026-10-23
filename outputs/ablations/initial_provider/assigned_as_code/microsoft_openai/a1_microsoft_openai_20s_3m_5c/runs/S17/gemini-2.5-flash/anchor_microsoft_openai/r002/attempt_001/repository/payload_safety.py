from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
import os

def check_payload_safety(decrypted_text: str, endpoint: str = None, key: str = None) -> dict:
    if not endpoint:
        endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        if not endpoint:
            raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable not set.")
    if not key:
        key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not key:
            raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Define categories to analyze
    categories = [
        TextCategory.HATE_SPEECH,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
        TextCategory.VIOLENCE,
    ]
    request = AnalyzeTextOptions(text=decrypted_text, categories=categories)

    response = client.analyze_text(request)

    safety_results = {"violations": []}
    for category_result in response.categories_analysis:
        if category_result.severity is not None and category_result.severity > 0:
            safety_results["violations"].append({
                "category": category_result.category.value,
                "severity": category_result.severity
            })

    return safety_results
