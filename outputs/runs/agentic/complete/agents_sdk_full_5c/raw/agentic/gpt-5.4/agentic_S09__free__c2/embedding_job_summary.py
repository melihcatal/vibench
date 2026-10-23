from __future__ import annotations

from openai import OpenAI


def embedding_job_summary(texts_embedded: int, model: str, elapsed_seconds: float) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize embedding batch execution in one concise sentence.",
            },
            {
                "role": "user",
                "content": f"Embedded {texts_embedded} texts using {model} in {elapsed_seconds:.2f} seconds.",
            },
        ],
    )
    return response.output_text.strip()
