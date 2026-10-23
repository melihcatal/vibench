from typing import Any, Dict

from openai import OpenAI


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this invoice note to {target_language}: {text}",
    )
    return {"translated_text": response.output_text, "provider": "openai", "model": "gpt-5.4-mini"}
