import os
from typing import Dict

from openai import OpenAI


def dashboard_note_translate(text: str, target_locale: str = "en") -> Dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this dashboard note to {target_locale}: {text}")
    return {"translated_text": response.output_text, "provider": "OpenAI", "model": "gpt-5.4-mini"}
