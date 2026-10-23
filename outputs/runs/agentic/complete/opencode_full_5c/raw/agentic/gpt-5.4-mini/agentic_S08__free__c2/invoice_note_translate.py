from typing import Any, Dict

from openai import OpenAI


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Translate to {target_language}: {text}"
    )
    return {"translation": response.output_text, "target_language": target_language}
