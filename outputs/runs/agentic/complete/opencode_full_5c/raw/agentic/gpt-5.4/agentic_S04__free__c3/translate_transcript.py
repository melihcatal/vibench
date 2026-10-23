from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def translate_transcript(
    segments: Iterable[Dict[str, Any]], target_language: str
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    normalized_segments: List[Dict[str, Any]] = list(segments)
    input_text = "\n".join(segment.get("text", "") for segment in normalized_segments)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate each transcript line into {target_language} and preserve order.",
            },
            {
                "role": "user",
                "content": input_text,
            },
        ],
    )
    translated_text = response.output_text
    translated_lines = translated_text.splitlines()
    translated_segments = []
    for index, segment in enumerate(normalized_segments):
        translated_segments.append(
            {
                **segment,
                "translated_text": translated_lines[index]
                if index < len(translated_lines)
                else "",
            }
        )
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODEL,
        "target_language": target_language,
        "segments": translated_segments,
    }
