import os
from typing import Optional

from openai import OpenAI


def translate_live_caption(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    system = "You translate live captions accurately and concisely. Return only the translated text."
    user = f"Translate the following caption into {target_language}."
    if source_language:
        user += f" The source language is {source_language}."
    user += f" Caption: {text}"
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
