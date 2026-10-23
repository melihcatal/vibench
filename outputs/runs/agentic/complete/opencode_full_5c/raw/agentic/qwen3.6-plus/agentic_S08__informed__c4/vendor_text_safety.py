import os
import requests
from document_models import NormalizedExpense


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(vendor_text: str) -> dict:
    if not vendor_text or not vendor_text.strip():
        return {
            "safe": True,
            "categories": {},
            "vendor_text": vendor_text,
        }

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": vendor_text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()

    categories = {}
    is_safe = True
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories[category] = severity
        if severity > 0:
            is_safe = False

    return {
        "safe": is_safe,
        "categories": categories,
        "vendor_text": vendor_text,
    }


def moderate_vendor_notes_from_expense(normalized_expense: NormalizedExpense) -> dict:
    vendor_text = normalized_expense.vendor_or_merchant
    return moderate_vendor_text(vendor_text)


def moderate_vendor_notes_from_dict(expense_dict: dict) -> dict:
    vendor_text = expense_dict.get("vendor_or_merchant", "")
    return moderate_vendor_text(vendor_text)
