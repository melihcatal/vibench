import os
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    source_clause = f" from {source_language}" if source_language else ""
    prompt = (
        f"Translate the following narration script{source_clause} into {target_language}. "
        "Preserve meaning, tone, formatting, line breaks, punctuation, and any SSML tags or placeholders exactly. "
        "Return only the translated script.\n\n"
        f"{text}"
    )
    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )
    return response.output_text.strip()
