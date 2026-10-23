import os
from openai import OpenAI
from typing import Optional


def translate_script(
    script: str, target_language: str = "Spanish", model: str = "gpt-4o-mini"
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator. Translate accurately while preserving narration style.",
            },
            {
                "role": "user",
                "content": f"Translate to {target_language}:\\n\\n{script}",
            },
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()
