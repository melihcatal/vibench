from __future__ import annotations

import os

from openai import OpenAI

MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def summarize_visual_analysis(results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize these visual analysis results in one short paragraph: {results}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize image-analysis outputs."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
