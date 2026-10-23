from typing import Any, Dict

from openai import OpenAI


def check_message_safety(payload_text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=[{"role": "user", "content": f"Assess this message text for unsafe content and return a concise yes/no plus reason: {payload_text}"}])
    return {"assessment": response.output_text, "safe": "unsafe" not in response.output_text.lower()}
