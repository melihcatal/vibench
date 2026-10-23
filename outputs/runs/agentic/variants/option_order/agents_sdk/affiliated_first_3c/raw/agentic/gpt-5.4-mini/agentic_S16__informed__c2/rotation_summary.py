from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


MODEL_ID = "gpt-4.1-mini"


def summarize_rotation_status(notes: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize secret rotation status clearly and concisely."},
            {"role": "user", "content": notes},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> str:
    notes = os.environ.get("ROTATION_NOTES", "Rotation completed successfully with no exceptions.")
    return summarize_rotation_status(notes)


if __name__ == "__main__":
    print(main())
