import os
from typing import Optional

from openai import OpenAI


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")
    source_part = f" from {source_language}" if source_language else ""
    prompt = (
        f"Translate the following identity-provider consent copy{source_part} into {target_language}. "
        f"Preserve meaning, legal intent, placeholders, product names, and tone. Return only the translated text.\n\n"
        f"{text}"
    )
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text
