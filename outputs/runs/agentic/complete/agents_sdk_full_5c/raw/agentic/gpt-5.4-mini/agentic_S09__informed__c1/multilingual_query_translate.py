from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_openai_client

TRANSLATION_MODEL = "gpt-4o-mini"


def translate_query(query: str, target_language: str = "en") -> str:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": "You translate search queries accurately and concisely."},
            {"role": "user", "content": f"Translate this query into {target_language}: {query}"},
        ],
    )
    return response.choices[0].message.content or ""
