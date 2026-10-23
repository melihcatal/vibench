from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


CLIENT = OpenAI()
MODEL = "gpt-4o-mini"


def translate_transcript(segments: Iterable[dict], target_language: str) -> List[dict]:
    translated = []
    for segment in segments:
        text = segment.get("text", "")
        prompt = f"Translate the following transcript segment into {target_language} while preserving meaning and speaker tags if present:\n{text}"
        response = CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You translate transcript segments faithfully."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        translated.append({
            **segment,
            "translated_text": response.choices[0].message.content,
        })
    return translated
