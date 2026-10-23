import os
from typing import Optional

from openai import OpenAI

from vision_client import build_openai_client

MODEL_ID = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def alt_text_translate(text: str, target_language: str, client: Optional[OpenAI] = None) -> str:
    client = client or build_openai_client()
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Translate image descriptions naturally while preserving meaning and brevity."},
            {"role": "user", "content": f"Translate this alt text into {target_language}: {text}"},
        ],
        temperature=0.2,
    )
    return response.output_text.strip()
