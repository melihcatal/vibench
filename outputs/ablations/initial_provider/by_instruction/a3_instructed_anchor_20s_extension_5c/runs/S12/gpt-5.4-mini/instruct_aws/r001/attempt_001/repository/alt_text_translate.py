import os
from typing import Dict

from openai import OpenAI


def alt_text_translate(text: str, target_language: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this image description to {target_language}: {text}",
    )
    return {"translated_text": resp.output_text}
