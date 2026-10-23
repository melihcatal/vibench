from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


def multilingual_query_translate(query: str, target_language: str) -> str:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {"role": "system", "content": "Translate user search queries accurately while preserving intent."},
            {"role": "user", "content": f"Translate this query into {target_language}: {query}"},
        ],
    )
    return response.choices[0].message.content or ""
