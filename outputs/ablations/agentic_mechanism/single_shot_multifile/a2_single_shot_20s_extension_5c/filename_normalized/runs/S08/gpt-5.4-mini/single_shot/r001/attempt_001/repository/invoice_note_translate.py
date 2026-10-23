import os
from typing import Any, Dict

from document_client import build_extract_client

OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
TARGET_LANGUAGE = os.getenv("INVOICE_NOTE_TARGET_LANGUAGE", "en")


def invoice_note_translate(note_payload: Dict[str, Any]) -> Dict[str, Any]:
    client = build_extract_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"Translate extracted invoice notes or descriptions into {TARGET_LANGUAGE}. Return JSON with translated_text and source_language."},
            {"role": "user", "content": __import__("json").dumps(note_payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return __import__("json").loads(response.choices[0].message.content or "{}")
