from __future__ import annotations

from openai import OpenAI

from embeddings_client import load_config


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate the user query into {target_language}. Preserve meaning and named entities."},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    return completion.choices[0].message.content or ""
