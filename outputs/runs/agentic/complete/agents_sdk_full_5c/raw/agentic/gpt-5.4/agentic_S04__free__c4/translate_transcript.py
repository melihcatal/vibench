from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import TranslationSegment

OPENAI_MODEL = "gpt-4o-mini"


def translate_transcript(segments: Iterable[str], target_language: str) -> List[dict]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results: List[dict] = []
    for segment in segments:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=f"Translate the following transcript segment into {target_language}:\n\n{segment}",
        )
        translated = response.output_text.strip()
        item = TranslationSegment(
            source_text=segment,
            translated_text=translated,
            target_language=target_language,
        )
        results.append(item.__dict__)
    return results
