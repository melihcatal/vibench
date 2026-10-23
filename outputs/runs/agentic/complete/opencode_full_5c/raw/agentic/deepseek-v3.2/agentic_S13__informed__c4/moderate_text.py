import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def moderate_text(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}

    response = client.analyze_text(request)

    result = {"text": text, "categories": {}}

    for category in response.categories_analysis:
        result["categories"][category.category] = {
            "severity": category.severity,
            "score": category.severity_score,
        }

    return result
