"""Check user-generated document fields for unsafe content using Perspective API.

Provider: Perspective API (REST)
Auth env: PERSPECTIVE_API_KEY
"""

from __future__ import annotations

import os
import requests
from typing import Any, Dict, List, Optional

from database_models import DocumentResponse


_PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def _extract_text_fields(record: DocumentResponse) -> List[str]:
    """Extract string-valued fields from a document that may contain user text."""
    texts = []
    for key, value in record.data.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            texts.append(value)
    return texts


def check_text_safety(
    records: List[DocumentResponse],
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Send document text fields to Perspective API for toxicity / safety analysis.

    Returns a list of per-record safety assessment results.
    """
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")

    requested_attrs = attributes or [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "INSULT",
        "PROFANITY",
        "THREAT",
    ]

    params = {"key": key}
    results: List[Dict[str, Any]] = []

    for record in records:
        texts = _extract_text_fields(record)
        record_safety: Dict[str, Any] = {
            "doc_id": record.doc_id,
            "fields_checked": [],
            "flagged": False,
            "scores": {},
        }

        for text in texts:
            body = {
                "comment": {"text": text},
                "requestedAttributes": {attr: {} for attr in requested_attrs},
                "languages": ["en"],
            }
            resp = requests.post(
                _PERSPECTIVE_API_URL,
                params=params,
                json=body,
                timeout=15,
            )
            resp.raise_for_status()
            analysis = resp.json()

            for attr_name, attr_data in analysis.get("attributeScores", {}).items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                record_safety["scores"][f"{attr_name}"] = round(score, 4)
                if score > 0.7:
                    record_safety["flagged"] = True

            record_safety["fields_checked"].append(text[:80])

        results.append(record_safety)

    return results


if __name__ == "__main__":
    sample = [
        DocumentResponse(doc_id="doc-1", data={"comment": "This is a harmless note."}, version=1, found=True),
    ]
    safety = check_text_safety(sample)
    for s in safety:
        print(f"{s['doc_id']}: flagged={s['flagged']}, scores={s['scores']}")
