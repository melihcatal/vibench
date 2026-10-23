from __future__ import annotations

from typing import Dict, Iterable, List

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def summarize_rotation_status(notes: Iterable[str]) -> str:
    client = OpenAI()
    prompt = "Summarize the secret rotation status in 2-4 concise bullet points. Notes:\n" + "\n".join(f"- {n}" for n in notes)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize operational secret rotation notes."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
