import os
from typing import Optional

from openai import OpenAI


def translate_result(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-5.4-mini")
    system_parts = [
        "You are a translation engine for model output.",
        "Return only the translated text.",
    ]
    if source_language:
        system_parts.append(f"Source language: {source_language}.")
    system_prompt = " ".join(system_parts)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate the following text into {target_language}:\n{text}"},
        ],
    )
    return response.output_text.strip()
