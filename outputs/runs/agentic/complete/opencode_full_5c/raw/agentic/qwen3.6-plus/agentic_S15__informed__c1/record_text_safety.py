import os
import requests
from database_models import DocumentResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
AZURE_API_VERSION = "2024-09-01"


def check_text_safety(text: str) -> dict:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {"text": text}
    response = requests.post(url, params=params, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def check_document_safety(documents: list[DocumentResponse]) -> list[dict]:
    results = []
    for doc in documents:
        fields_to_check = []
        for key, value in doc.data.items():
            if isinstance(value, str) and len(value) > 0:
                fields_to_check.append({"field": key, "value": value})
        doc_safety = {
            "document_id": doc.document_id,
            "collection": doc.collection,
            "field_results": [],
        }
        for field_item in fields_to_check:
            safety_result = check_text_safety(field_item["value"])
            doc_safety["field_results"].append(
                {
                    "field": field_item["field"],
                    "analysis": safety_result,
                }
            )
        results.append(doc_safety)
    return results
