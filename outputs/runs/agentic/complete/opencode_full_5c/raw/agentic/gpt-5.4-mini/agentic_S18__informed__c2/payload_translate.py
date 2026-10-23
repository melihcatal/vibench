from typing import Dict

from openai import OpenAI


def payload_translate(text: str, target_language: str, model: str = "gpt-5.4-mini") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(model=model, input=f"Translate to {target_language}: {text}")
    return {"provider": "openai", "model": model, "translation": response.output_text}
