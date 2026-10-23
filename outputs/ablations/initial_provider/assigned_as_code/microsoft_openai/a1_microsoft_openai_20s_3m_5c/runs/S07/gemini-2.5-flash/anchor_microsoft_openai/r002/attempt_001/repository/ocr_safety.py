import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from document_models import SafetyResult

def ocr_safety(text: str, config=None) -> SafetyResult:
    if config is None:
        config = {}

    key = config.get('content_safety_api_key') or os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = config.get('content_safety_endpoint') or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not all([key, endpoint]):
        raise ValueError("Azure Content Safety API key and endpoint must be provided in config or environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    is_safe = True
    categories = {
        "Hate": {"severity": 0, "detected": False},
        "Sexual": {"severity": 0, "detected": False},
        "Violence": {"severity": 0, "detected": False},
        "SelfHarm": {"severity": 0, "detected": False},
    }

    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        severity = category_result.severity
        if severity > 0:
            is_safe = False
            categories[category_name]["detected"] = True
            categories[category_name]["severity"] = severity

    return SafetyResult(is_safe=is_safe, categories=categories)
