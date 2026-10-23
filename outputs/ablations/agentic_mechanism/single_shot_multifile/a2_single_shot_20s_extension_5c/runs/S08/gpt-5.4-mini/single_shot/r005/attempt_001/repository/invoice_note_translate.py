from typing import Any, Dict

from openai import OpenAI

from document_client import load_document_settings
from document_models import coerce_text_payload


def invoice_note_translate(notes: Any, target_language: str = "en") -> Dict[str, Any]:
    settings = load_document_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": f"Translate invoice notes to {target_language}. Return JSON only."},
            {"role": "user", "content": coerce_text_payload(notes)},
        ],
        text={"format": {"type": "json_object"}},
    )
    return {"translated_text": getattr(response, "output_text", "")}
