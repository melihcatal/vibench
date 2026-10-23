from __future__ import annotations

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def summarize_message_results(results: list[dict] | str) -> str:
    client = OpenAI()
    prompt = f"Summarize these message processing results briefly and clearly: {results}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize pub/sub processing outcomes."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
