import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def translate_invoice_note(note: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    note = _normalize_text(note)
    if not note:
        return ""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = (
        "You translate short invoice notes, memo fields, and descriptions. "
        "Return only the translated text, preserving numbers, dates, codes, currency amounts, and proper nouns when appropriate."
    )
    user_prompt = {
        "target_language": target_language,
        "source_language": source_language,
        "text": note,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_invoice_notes(notes: List[str], target_language: str = "en", source_language: Optional[str] = None) -> List[str]:
    return [translate_invoice_note(note, target_language=target_language, source_language=source_language) for note in notes]
