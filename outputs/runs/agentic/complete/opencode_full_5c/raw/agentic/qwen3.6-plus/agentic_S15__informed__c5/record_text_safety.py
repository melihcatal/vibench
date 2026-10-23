import os
import requests
from database_models import DocumentResponse


CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip(
    "/"
)
CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"


def check_text_safety(text, categories=None):
    if not text or not text.strip():
        return {"safe": True, "categories": {}, "text": text}

    endpoint = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    if categories:
        payload["categories"] = categories

    response = requests.post(
        endpoint, headers=headers, params=params, json=payload, timeout=30
    )
    response.raise_for_status()
    result = response.json()

    category_scores = {}
    flagged = False
    for category_result in result.get("categoriesAnalysis", []):
        cat = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        category_scores[cat] = severity
        if severity >= 4:
            flagged = True

    return {
        "safe": not flagged,
        "categories": category_scores,
        "text": text,
        "blocklistsMatch": result.get("blocklistsMatch", []),
    }


def check_document_safety(document, text_fields=None):
    if isinstance(document, DocumentResponse):
        data = document.data
        doc_id = document.document_id
    elif isinstance(document, dict):
        data = document
        doc_id = document.get("document_id", document.get("id", "unknown"))
    else:
        raise ValueError("document must be a DocumentResponse or dict")

    if text_fields is None:
        text_fields = [k for k, v in data.items() if isinstance(v, str)]

    results = {}
    overall_safe = True
    for field_name in text_fields:
        field_value = data.get(field_name, "")
        if not field_value:
            continue
        safety_result = check_text_safety(field_value)
        results[field_name] = safety_result
        if not safety_result["safe"]:
            overall_safe = False

    return {
        "document_id": doc_id,
        "safe": overall_safe,
        "field_results": results,
    }
