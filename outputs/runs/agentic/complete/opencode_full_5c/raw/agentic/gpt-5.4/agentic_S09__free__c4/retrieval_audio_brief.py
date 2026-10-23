from __future__ import annotations

import base64
import os
from collections.abc import Sequence

from openai import OpenAI


OPENAI_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-audio-preview")
OPENAI_AUDIO_VOICE = os.getenv("OPENAI_AUDIO_VOICE", "alloy")


def retrieval_audio_brief(
    query: str, retrieved_results: Sequence[dict[str, object]]
) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    bullets = "\n".join(
        f"- {item.get('document', '')} (score={item.get('score', 0)})"
        for item in list(retrieved_results)[:5]
    )
    response = client.responses.create(
        model=OPENAI_AUDIO_MODEL,
        modalities=["text", "audio"],
        audio={"voice": OPENAI_AUDIO_VOICE, "format": "mp3"},
        input=[
            {
                "role": "system",
                "content": "Create a short spoken retrieval brief that highlights the most relevant findings for a search query.",
            },
            {
                "role": "user",
                "content": f"Query: {query}\nRetrieved results:\n{bullets}",
            },
        ],
    )
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if getattr(content, "type", None) == "output_audio":
                    return base64.b64decode(content.audio)
    return b""
