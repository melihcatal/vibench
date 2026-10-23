import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_INVOICE_NOTE_TRANSLATE_MODEL", "gpt-4.1-mini")


def translate_invoice_note(note: str, target_language: str = "English", model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "You translate invoice notes or descriptions accurately and concisely.",
            },
            {
                "role": "user",
                "content": (
                    f"Translate the following invoice note or description into {target_language}. "
                    "Preserve names, amounts, dates, and invoice-specific terminology where appropriate. "
                    "Return only the translated text.\n\n"
                    f"Note: {note}"
                ),
            },
        ],
    )
    return response.output_text


def translate_invoice_note_json(note: str, target_language: str = "English", model: Optional[str] = None) -> Dict[str, Any]:
    translated = translate_invoice_note(note, target_language=target_language, model=model)
    return {"translated_note": translated, "provider": "openai", "model": model or DEFAULT_MODEL, "target_language": target_language}
