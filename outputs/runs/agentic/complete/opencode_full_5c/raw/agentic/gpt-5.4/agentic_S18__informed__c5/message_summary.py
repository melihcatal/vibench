from __future__ import annotations

from openai import OpenAI


def summarize_message_processing(result: dict) -> dict[str, str]:
    client = OpenAI()
    completion = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize message processing outcomes in one concise sentence for operators.",
            },
            {
                "role": "user",
                "content": str(result),
            },
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": completion.output_text,
    }
