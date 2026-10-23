from __future__ import annotations

from typing import Dict, List

from speech_client import OPENAI_TEXT_MODEL, SpeechClientFactory


def translate_transcript(segments: List[Dict[str, str]], target_language: str) -> str:
    client = SpeechClientFactory.create()
    transcript = "\n".join(segment.get("text", "") for segment in segments)
    response = client.responses.create(
        model=OPENAI_TEXT_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate transcript segments into {target_language} without adding commentary.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.output_text
