from __future__ import annotations

from openai import OpenAI

from embeddings_client import load_settings


def multilingual_query_translate(query: str, target_language: str = "English") -> str:
    settings = load_settings()
    client = OpenAI()
    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": "You translate search queries accurately and tersely."},
            {
                "role": "user",
                "content": f"Translate this query into {target_language} for semantic search: {query}",
            },
        ],
    )
    return response.choices[0].message.content.strip()
