import os
import requests
from model_models import SafetyCheckResult

def check_azure_content_safety(text: str) -> SafetyCheckResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    data = {"text": text}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # Example of parsing the result; adjust based on actual API response structure
    # Assuming any non-zero severity for any category means unsafe.
    is_safe = True
    categories = {}
    for category_analysis in result.get('categoriesAnalysis', []):
        category = category_analysis['category']
        severity = category_analysis['severity']
        categories[category] = f"Severity: {severity}"
        if severity > 0:
            is_safe = False

    return SafetyCheckResult(is_safe=is_safe, categories=categories, raw_response=result)
