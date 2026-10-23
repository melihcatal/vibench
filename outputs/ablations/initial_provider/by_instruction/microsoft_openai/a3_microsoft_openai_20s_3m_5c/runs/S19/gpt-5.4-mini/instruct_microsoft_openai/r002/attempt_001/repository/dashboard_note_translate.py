from typing import Any, Dict

from openai import OpenAI


def dashboard_note_translate(text: str, target_locale: str) -> Dict[str, Any]:
    client = OpenAI(api_key="")
    result = client.responses.create(model="gpt-5.4-mini", input=f"Translate to {target_locale}: {text}")
    return {"provider": "OpenAI", "result": result.model_dump()}
