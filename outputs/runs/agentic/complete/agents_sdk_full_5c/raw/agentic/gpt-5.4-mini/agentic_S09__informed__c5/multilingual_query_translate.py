from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_client


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client: OpenAI = get_client()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Translate user queries accurately while preserving search intent."},
            {"role": "user", "content": f"Translate this query into {target_language}: {query}"},
        ],
    )
    return response.choices[0].message.content or ""
