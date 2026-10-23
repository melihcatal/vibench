from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import normalize_transcript_text


OPENAI_MODEL = "gpt-4.1-mini"


def translate_live_captions(captions: Iterable[str], target_language: str = "es") -> List[str]:
    client = OpenAI()
    translated: List[str] = []
    for caption in captions:
        text = normalize_transcript_text(caption)
        if not text:
            continue
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"Translate live speech captions into {target_language}."},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        translated.append(response.choices[0].message.content or "")
    return translated
