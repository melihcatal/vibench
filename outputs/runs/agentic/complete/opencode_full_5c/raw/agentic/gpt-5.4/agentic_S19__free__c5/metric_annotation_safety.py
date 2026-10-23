from __future__ import annotations

import json

from observability_client import extract_gemini_text, gemini_generate


def metric_annotation_safety(text: str) -> dict:
    prompt = json.dumps(
        {
            "task": "Classify monitoring annotation safety",
            "text": text,
            "policy": "Detect harassment, hate, sexual content, dangerous content, self-harm, or secrets.",
            "instructions": "Return JSON with keys safe, categories, rationale.",
        }
    )
    response = gemini_generate("gemini-1.5-flash", prompt)
    output = extract_gemini_text(response)
    return (
        json.loads(output)
        if output
        else {"safe": True, "categories": [], "rationale": ""}
    )
