from __future__ import annotations

from typing import Dict

from google import genai

GEMINI_MODEL = "gemini-2.0-flash"


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, str]:
    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"Translate the following invoice note into {target_language}: {text}",
    )
    return {"translated_text": response.text or "", "model": GEMINI_MODEL}
