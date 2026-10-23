from typing import Dict
from document_client import get_openai_client

TRANSLATION_MODEL = "gpt-4.1-mini"


def translate_invoice_note(note_text: str, target_language: str = "en") -> Dict[str, str]:
    client = get_openai_client()
    prompt = (
        f"Translate this invoice note into {target_language}. Preserve any amounts, dates, and names. "
        "Return JSON with keys translated_text and detected_language.\n\n"
        f"Note:\n{note_text}"
    )
    response = client.responses.create(model=TRANSLATION_MODEL, input=prompt, temperature=0)
    return {"translated_text": response.output_text, "detected_language": "unknown"}
