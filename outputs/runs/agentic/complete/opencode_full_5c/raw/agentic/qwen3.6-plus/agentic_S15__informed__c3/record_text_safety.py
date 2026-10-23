import os
import requests
from database_models import FetchResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_text_safety(text: str, categories: list[str] | None = None) -> dict:
    if not text or not text.strip():
        return {
            "provider": "azure_ai_content_safety",
            "safe": True,
            "flags": [],
            "scores": {},
            "message": "Empty text provided",
        }

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    payload = {"text": text, "outputType": "FourSeverityLevels"}

    if categories:
        payload["categories"] = categories

    response = requests.post(
        url, params=params, headers=headers, json=payload, timeout=30
    )
    response.raise_for_status()

    result = response.json()

    flags = []
    scores = {}
    is_safe = True

    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        scores[category] = severity
        if severity >= 2:
            flags.append({"category": category, "severity": severity})
            is_safe = False

    return {
        "provider": "azure_ai_content_safety",
        "safe": is_safe,
        "flags": flags,
        "scores": scores,
        "blocklistsMatch": result.get("blocklistsMatch", []),
    }


def check_document_safety(
    document_data: dict, text_fields: list[str] | None = None
) -> dict:
    if text_fields is None:
        text_fields = [
            "title",
            "content",
            "description",
            "body",
            "text",
            "comment",
            "message",
        ]

    results = {}
    overall_safe = True
    all_flags = []

    for field_name in text_fields:
        if field_name in document_data and document_data[field_name]:
            field_text = document_data[field_name]
            if isinstance(field_text, str) and field_text.strip():
                safety_result = check_text_safety(field_text)
                results[field_name] = safety_result
                if not safety_result["safe"]:
                    overall_safe = False
                    all_flags.extend(safety_result["flags"])

    return {
        "provider": "azure_ai_content_safety",
        "document_safe": overall_safe,
        "field_results": results,
        "total_flags": len(all_flags),
        "flags": all_flags,
    }


def check_fetch_response_safety(fetch_response: FetchResponse) -> dict:
    if not fetch_response.found or not fetch_response.data:
        return {
            "provider": "azure_ai_content_safety",
            "document_safe": True,
            "field_results": {},
            "total_flags": 0,
            "flags": [],
            "message": "No document data to check",
        }
    return check_document_safety(fetch_response.data)


if __name__ == "__main__":
    sample_doc = {
        "title": "Sample Document",
        "content": "This is a safe and normal document content.",
        "status": "active",
    }
    result = check_document_safety(sample_doc)
    print(result)
