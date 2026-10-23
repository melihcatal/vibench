import os
from typing import Optional

from openai import OpenAI


def result_translate(text: str, target_language: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Translate the provided model output into the requested language while preserving meaning, tone, and formatting.",
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\n\nText:\n{text}",
            },
        ],
        temperature=0,
    )
    return response.output_text
