from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_openai_client


TRANSLATION_MODEL = "gpt-4o-mini"


def multilingual_query_translate(query: str, target_language: str = "English", model: str = TRANSLATION_MODEL) -> str:
    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Translate search queries faithfully for multilingual semantic retrieval.",
            },
            {
                "role": "user",
                "content": f"Translate this query to {target_language}: {query}",
            },
        ],
    )
    return response.output_text.strip()
