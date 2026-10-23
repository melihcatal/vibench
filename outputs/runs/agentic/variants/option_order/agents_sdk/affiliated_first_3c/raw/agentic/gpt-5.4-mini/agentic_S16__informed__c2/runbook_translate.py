from __future__ import annotations

import os
from typing import List

from openai import OpenAI


MODEL_ID = "gpt-4.1-mini"


def translate_runbook(notes: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Translate operational runbook notes faithfully and preserve technical meaning."},
            {"role": "user", "content": f"Translate into {target_language}: {notes}"},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> str:
    notes = os.environ.get("RUNBOOK_NOTES", "Rotate secrets every 90 days and validate downstream services.")
    target_language = os.environ.get("RUNBOOK_TARGET_LANGUAGE", "Spanish")
    return translate_runbook(notes, target_language)


if __name__ == "__main__":
    print(main())
