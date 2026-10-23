from typing import Dict

from openai import OpenAI


def message_safety(text: str, model: str = "gpt-5.4-mini") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(model=model, input=f"Assess safety of: {text}")
    return {"provider": "openai", "model": model, "assessment": response.output_text}
