from __future__ import annotations

import os

from openai import OpenAI

MODEL_ID = os.getenv("LLM_TTS_SUMMARY_MODEL", "gpt-4.1-mini")


def spoken_brief(model_output: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Convert the model output into a short spoken brief."},
            {"role": "user", "content": model_output},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
