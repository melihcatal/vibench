from __future__ import annotations

from openai import OpenAI


def multilingual_query_translate(
    query: str, target_language: str, model: str = "gpt-4o-mini"
) -> dict:
    client = OpenAI(
        api_key=__import__("os").getenv("OPENAI_API_KEY"),
        base_url=__import__("os").getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ),
    )
    completion = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate search queries faithfully and keep named entities intact.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Translate into {target_language}: {query}",
                    }
                ],
            },
        ],
    )
    return {
        "provider": "openai",
        "model": model,
        "translated_query": completion.output_text,
        "target_language": target_language,
    }
