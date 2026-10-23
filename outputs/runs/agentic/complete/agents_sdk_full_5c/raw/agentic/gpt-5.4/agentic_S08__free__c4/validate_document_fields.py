from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
REQUIRED_FIELDS = {
    "invoice": ["vendor", "invoice_date", "total", "line_items"],
    "receipt": ["merchant", "tax", "total", "items"],
}


def validate_document_fields(extracted: Dict[str, Any], min_confidence: float = 0.5) -> Dict[str, Any]:
    doc_type = extracted.get("document_type", "invoice")
    required = REQUIRED_FIELDS.get(doc_type, [])
    missing: List[str] = [field for field in required if not extracted.get(field)]

    confidence = extracted.get("confidence", {}) or {}
    low_confidence = {
        field: score for field, score in confidence.items() if score is not None and score < min_confidence
    }

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Assess whether extracted structured document fields appear complete and internally consistent. Return JSON with keys valid, issues, recommended_fixes.",
            },
            {
                "role": "user",
                "content": str({"document": extracted, "missing": missing, "low_confidence": low_confidence}),
            },
        ],
    )
    provider_assessment = __import__("json").loads(completion.choices[0].message.content)
    return {
        "valid": provider_assessment.get("valid", not missing and not low_confidence),
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "issues": provider_assessment.get("issues", []),
        "recommended_fixes": provider_assessment.get("recommended_fixes", []),
    }
