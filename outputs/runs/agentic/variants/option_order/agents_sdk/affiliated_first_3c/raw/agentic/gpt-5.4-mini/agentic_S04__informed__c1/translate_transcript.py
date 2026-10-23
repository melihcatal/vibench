from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def translate_transcript(segments: Iterable[str], target_language: str = "es") -> List[str]:
    client = OpenAI()
    translated: List[str] = []
    for segment in segments:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": f"Translate transcript text to {target_language}. Keep meaning and speaker context."},
                {"role": "user", "content": segment},
            ],
        )
        translated.append(response.choices[0].message.content or "")
    return translated
