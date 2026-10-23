from __future__ import annotations

from safety_client import deepgram_post


def reviewer_brief_audio(text: str, voice: str = "aura-asteria-en") -> bytes:
    payload = {"text": text}
    response = deepgram_post(f"/v1/speak?model={voice}", payload)
    return response.content
