from __future__ import annotations

from typing import Iterable

from speech_client import client


def stream_with_language(audio_frames: Iterable[bytes], language_code: str = "en-GB"):
    responses = client.recognize_stream(audio_frames, language_code=language_code, enable_punctuation=True, model="latest_long")
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield {
                    "transcript": result.alternatives[0].transcript,
                    "final": result.is_final,
                    "language_code": language_code,
                }
