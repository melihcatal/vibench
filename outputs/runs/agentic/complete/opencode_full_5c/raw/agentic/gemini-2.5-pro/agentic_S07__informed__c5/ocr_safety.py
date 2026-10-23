import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from document_models import SafetyAnalysis


def ocr_safety(text: str) -> SafetyAnalysis:
    """
    Checks extracted document text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        # Handle potential exceptions from the API call
        return SafetyAnalysis(is_safe=False, categories={"error": str(e)})

    is_safe = all(category.severity == 0 for category in response.categories_analysis)

    categories_result = {
        cat.category.value: {"severity": cat.severity}
        for cat in response.categories_analysis
    }

    return SafetyAnalysis(is_safe=is_safe, categories=categories_result)
