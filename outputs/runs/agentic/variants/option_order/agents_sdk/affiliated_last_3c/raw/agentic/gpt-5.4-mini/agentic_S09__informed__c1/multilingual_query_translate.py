from __future__ import annotations

from openai import OpenAI

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_query(query: str, target_language: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"Translate the user's query into {target_language} without commentary."},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    return completion.choices[0].message.content or ""
