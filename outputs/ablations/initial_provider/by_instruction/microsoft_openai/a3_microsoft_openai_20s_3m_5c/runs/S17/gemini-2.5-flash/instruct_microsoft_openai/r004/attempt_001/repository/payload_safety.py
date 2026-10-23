import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_payload_safety(decrypted_text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Categories to check for unsafe content
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
        TextCategory.VIOLENCE
    ]

    request = AnalyzeTextOptions(text=decrypted_text, categories=categories)
    response = client.analyze_text(request)

    safety_results = []
    for category_result in response.categories_analysis:
        safety_results.append({
            "category": category_result.category.value,
            "severity": category_result.severity
        })

    return {"safety_results": safety_results}

