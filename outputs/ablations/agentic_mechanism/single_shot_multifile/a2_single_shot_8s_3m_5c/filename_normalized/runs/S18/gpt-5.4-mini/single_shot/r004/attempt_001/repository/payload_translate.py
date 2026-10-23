from typing import Any, Dict

from openai import OpenAI


def translate_payload_text(payload_text: str, target_language: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=[{"role": "user", "content": f"Translate this customer-facing message into {target_language}: {payload_text}"}])
    return {"translated_text": response.output_text, "target_language": target_language}
