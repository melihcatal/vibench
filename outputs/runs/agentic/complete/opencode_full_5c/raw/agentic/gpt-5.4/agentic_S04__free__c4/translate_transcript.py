from __future__ import annotations

import os

from openai import OpenAI


def translate_transcript(
    segments: list[dict[str, object]], target_language: str
) -> dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    joined_segments = "\n".join(str(segment.get("text", "")) for segment in segments)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate transcript segments into {target_language} and preserve order.",
            },
            {"role": "user", "content": joined_segments},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "translated_text": response.output_text,
    }
