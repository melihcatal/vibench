from __future__ import annotations

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "English") -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate the user's search query into {target_language}. Return only the translated query.",
            },
            {
                "role": "user",
                "content": query,
            },
        ],
    )
    return response.output_text.strip()
