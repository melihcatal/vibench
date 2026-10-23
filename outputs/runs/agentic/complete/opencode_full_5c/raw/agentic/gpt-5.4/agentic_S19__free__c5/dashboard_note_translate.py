from __future__ import annotations

import json

from observability_client import extract_gemini_text, gemini_generate


def dashboard_note_translate(text: str, target_locale: str) -> dict:
    prompt = json.dumps(
        {
            "task": "Translate dashboard note",
            "text": text,
            "target_locale": target_locale,
            "instructions": "Return JSON with keys translated_text and target_locale.",
        }
    )
    response = gemini_generate("gemini-1.5-flash", prompt, temperature=0.1)
    output = extract_gemini_text(response)
    return (
        json.loads(output)
        if output
        else {"translated_text": "", "target_locale": target_locale}
    )
