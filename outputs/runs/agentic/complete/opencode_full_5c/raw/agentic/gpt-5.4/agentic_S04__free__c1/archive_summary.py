from __future__ import annotations

import os
from typing import Any, Dict, Iterable

from openai import OpenAI


def summarize_transcription_for_archive(segments: Iterable[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    joined_segments = "\n".join(segments)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize batch transcription results for archival storage in a concise structured paragraph.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": joined_segments}],
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
        "response_id": response.id,
    }
