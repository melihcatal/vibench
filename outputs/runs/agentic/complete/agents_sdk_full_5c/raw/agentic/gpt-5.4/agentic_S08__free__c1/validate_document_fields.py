from __future__ import annotations

from typing import Any, Dict, List

import requests

from document_client import post_openai_responses, first_content_text


OPENAI_MODEL = "gpt-4.1-mini"


def validate_document_fields(document_payload: Dict[str, Any], min_confidence: float = 0.6) -> Dict[str, Any]:
    required = ["total", "items"]
    if document_payload.get("document_type") == "invoice":
        required.extend(["vendor", "invoice_date"])
    elif document_payload.get("document_type") == "receipt":
        required.extend(["merchant", "tax"])

    missing = [field for field in required if document_payload.get(field) in (None, "", [])]
    low_conf_items: List[Dict[str, Any]] = []
    for item in document_payload.get("items", []):
        confidence = item.get("confidence")
        if confidence is not None and confidence < min_confidence:
            low_conf_items.append(item)

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Assess whether a structured accounting document extraction is valid. Return compact JSON with summary, issues, and recommended_action.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": str({
                            "document": document_payload,
                            "missing": missing,
                            "low_confidence_items": low_conf_items,
                            "threshold": min_confidence,
                        }),
                    }
                ],
            },
        ],
    }
    analysis = post_openai_responses(payload)
    return {
        "valid": not missing and not low_conf_items,
        "missing_fields": missing,
        "low_confidence_items": low_conf_items,
        "llm_review": first_content_text(analysis),
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
