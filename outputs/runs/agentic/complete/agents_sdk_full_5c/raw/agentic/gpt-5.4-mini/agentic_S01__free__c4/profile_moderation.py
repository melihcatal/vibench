from __future__ import annotations

import os

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Classify profile text for safety and policy concerns. Return concise JSON only.",
            },
            {"role": "user", "content": profile_text},
        ],
    )
    return {"result": response.output_text}
