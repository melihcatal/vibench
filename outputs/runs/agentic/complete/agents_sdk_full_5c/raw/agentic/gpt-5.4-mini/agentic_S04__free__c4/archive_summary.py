from __future__ import annotations

from typing import Dict, List

from speech_client import OPENAI_TEXT_MODEL, SpeechClientFactory


def archive_summary(segments: List[Dict[str, str]]) -> str:
    client = SpeechClientFactory.create()
    transcript = "\n".join(segment.get("text", "") for segment in segments)
    response = client.responses.create(
        model=OPENAI_TEXT_MODEL,
        input=[
            {"role": "system", "content": "Summarize this transcription result for archival notes."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.output_text
