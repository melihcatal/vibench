from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_INVOICE_NOTE_TRANSLATION_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _extract_text(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("note"), str):
        return payload["note"]
    if isinstance(payload.get("notes"), str):
        return payload["notes"]
    if isinstance(payload.get("description"), str):
        return payload["description"]
    if isinstance(payload.get("text"), str):
        return payload["text"]
    return ""


def translate_invoice_note(note: str, target_language: str = "en") -> Dict[str, Any]:
    if not note:
        return {"translated_text": None, "source_text": None, "target_language": target_language}
    response = _client().responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate invoice notes or descriptions while preserving meaning, numbers, dates, and proper nouns. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": json.dumps({"text": note, "target_language": target_language}),
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    content = response.output_text or ""
    if not content:
        return {"translated_text": None, "source_text": note, "target_language": target_language}
    data = json.loads(content)
    if not isinstance(data, dict):
        return {"translated_text": str(data), "source_text": note, "target_language": target_language}
    translated_text = data.get("translated_text") or data.get("translation") or data.get("text")
    return {
        "translated_text": translated_text,
        "source_text": note,
        "target_language": target_language,
    }


def translate_invoice_note_from_mapping(payload: Dict[str, Any], target_language: str = "en") -> Dict[str, Any]:
    return translate_invoice_note(_extract_text(payload), target_language=target_language)


__all__ = ["OPENAI_TRANSLATION_MODEL", "translate_invoice_note", "translate_invoice_note_from_mapping"]
