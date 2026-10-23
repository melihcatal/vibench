import os
from typing import Any, Dict, List, Optional

import requests

from database_models import DocumentResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_text_safety(
    documents: List[Dict[str, Any]],
    text_fields: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
) -> DocumentResponse:
    if not documents:
        return DocumentResponse(
            success=False,
            error="No documents provided for safety check",
        )

    if not AZURE_CONTENT_SAFETY_KEY:
        return DocumentResponse(
            success=False,
            error="AZURE_CONTENT_SAFETY_KEY environment variable is not set",
        )

    text_fields = text_fields or [
        "title",
        "content",
        "description",
        "body",
        "text",
        "message",
    ]
    categories = categories or ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    results = []
    overall_safe = True

    for doc in documents:
        doc_id = doc.get("id", doc.get("_id", "unknown"))
        texts_to_check = []

        for field in text_fields:
            if field in doc and isinstance(doc[field], str) and doc[field].strip():
                texts_to_check.append({"field": field, "text": doc[field]})

        if not texts_to_check:
            results.append(
                {
                    "document_id": doc_id,
                    "safe": True,
                    "categories": {},
                    "detail": "No text fields found to analyze",
                }
            )
            continue

        doc_safe = True
        doc_categories = {}

        for text_item in texts_to_check:
            payload = {
                "text": text_item["text"],
                "categories": categories,
                "outputType": "FourSeverityLevels",
            }

            try:
                response = requests.post(
                    url, params=params, headers=headers, json=payload
                )
                response.raise_for_status()
                analysis = response.json()

                field_categories = {}
                for category_result in analysis.get("categoriesAnalysis", []):
                    cat_name = category_result.get("category", "Unknown")
                    severity = category_result.get("severity", 0)
                    field_categories[cat_name] = severity
                    if severity >= 4:
                        doc_safe = False
                        overall_safe = False

                doc_categories[text_item["field"]] = field_categories

            except requests.exceptions.RequestException as exc:
                doc_safe = False
                doc_categories[text_item["field"]] = {"error": str(exc)}

        results.append(
            {
                "document_id": doc_id,
                "safe": doc_safe,
                "categories": doc_categories,
            }
        )

    return DocumentResponse(
        success=True,
        document={
            "overall_safe": overall_safe,
            "total_documents": len(documents),
            "results": results,
            "service": "Azure AI Content Safety",
        },
    )
