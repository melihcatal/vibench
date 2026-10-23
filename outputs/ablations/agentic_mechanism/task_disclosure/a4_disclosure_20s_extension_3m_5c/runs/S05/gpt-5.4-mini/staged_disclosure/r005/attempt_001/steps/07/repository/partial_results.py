import os
from dataclasses import dataclass
from typing import Callable, Optional

import httpx


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"


@dataclass(frozen=True)
class RecognitionEvent:
    text: str
    is_final: bool


def _openai_client() -> httpx.Client:
    api_key = os.environ["OPENAI_API_KEY"]
    return httpx.Client(
        timeout=60.0,
        headers={"Authorization": f"Bearer {api_key}"},
    )


def handle_recognition_event(
    audio_chunk: bytes,
    *,
    on_partial: Optional[Callable[[str], None]] = None,
    on_final: Optional[Callable[[str], None]] = None,
    model: str = "whisper-1",
) -> RecognitionEvent:
    with _openai_client() as client:
        response = client.post(
            OPENAI_TRANSCRIBE_URL,
            data={"model": model},
            files={"file": ("chunk.wav", audio_chunk, "audio/wav")},
        )
        response.raise_for_status()
        payload = response.json()

    text = str(payload.get("text", "")).strip()
    is_final = bool(payload.get("is_final", True))

    if is_final:
        if on_final is not None:
            on_final(text)
    else:
        if on_partial is not None:
            on_partial(text)

    return RecognitionEvent(text=text, is_final=is_final)
