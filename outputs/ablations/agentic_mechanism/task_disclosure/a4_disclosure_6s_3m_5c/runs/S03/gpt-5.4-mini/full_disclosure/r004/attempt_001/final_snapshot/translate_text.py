import os
from typing import Optional

from openai import OpenAI


def translate_text(text: str, source_language: str, target_language: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or "gpt-5.4-mini"
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a translation engine. Translate the user's text from "
                    f"{source_language} to {target_language}. Return only the translated text."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text.strip()
