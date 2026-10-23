import os
from typing import Any

from openai import OpenAI

from safety_client import get_openai_client, normalize_text_input


def appeal_translate(text: Any, target_language: str = "en") -> str:
    client: OpenAI = get_openai_client()
    prompt = f"Translate this moderation appeal into {target_language}: {normalize_text_input(text)}"
    response = client.responses.create(
        model=os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"), input=prompt
    )
    return response.output_text
