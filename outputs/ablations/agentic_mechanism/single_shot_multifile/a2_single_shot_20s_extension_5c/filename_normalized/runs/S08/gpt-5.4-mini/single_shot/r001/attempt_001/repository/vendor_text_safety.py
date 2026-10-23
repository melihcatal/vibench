import os
from typing import Any, Dict

from document_client import build_extract_client

OPENAI_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")


def vendor_text_safety(vendor_notes: Dict[str, Any]) -> Dict[str, Any]:
    client = build_extract_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Moderate vendor notes or memo fields for safety and policy issues. Return JSON with safe, category, and reasons."},
            {"role": "user", "content": __import__("json").dumps(vendor_notes, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return __import__("json").loads(response.choices[0].message.content or "{}")
