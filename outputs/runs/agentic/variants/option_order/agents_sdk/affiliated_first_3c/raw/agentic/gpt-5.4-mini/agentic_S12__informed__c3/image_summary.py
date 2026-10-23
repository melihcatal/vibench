from __future__ import annotations

import os

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_ID = "gpt-4o-mini"


def summarize_visual_results(labels, description, text_lines):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Labels: {labels}\nDescription: {description}\nText: {text_lines}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize image analysis results concisely."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
