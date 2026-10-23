import os
from typing import Any, Dict

from openai import OpenAI


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": f"Translate to {target_language}: {text}"}])
    return {"translated_text": response.choices[0].message.content, "provider": "openai"}
