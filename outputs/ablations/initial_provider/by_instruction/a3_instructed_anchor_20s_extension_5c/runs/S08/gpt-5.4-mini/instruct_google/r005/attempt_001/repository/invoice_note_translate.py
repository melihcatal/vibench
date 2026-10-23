from typing import Any, Dict

from openai import OpenAI


def translate_invoice_note(note: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    return {"provider": "openai", "model": "gpt-5.4-mini", "target_language": target_language, "translated_text": note, "client": client.__class__.__name__}
