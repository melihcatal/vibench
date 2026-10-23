from __future__ import annotations

import io
from typing import Iterator, Optional

from speech_client import SpeechClientConfig, StreamingSpeechClient
from speech_models import NormalizedTranscriptEvent


def stream_with_language(audio_stream: io.BufferedIOBase, language: str, punctuation: bool = True, config: Optional[SpeechClientConfig] = None) -> Iterator[NormalizedTranscriptEvent]:
    base = config or SpeechClientConfig.from_env()
    merged = SpeechClientConfig(
        api_key=base.api_key,
        model=base.model,
        sample_rate=base.sample_rate,
        format=base.format,
        language=language,
        punctuation=punctuation,
    )
    client = StreamingSpeechClient(merged)
    recognizer = client.start_recognizer(language=language, enable_punctuation=punctuation)
    recognizer.start()
    while True:
        chunk = audio_stream.read(3200)
        if not chunk:
            break
        recognizer.send(chunk)
        for event in getattr(client, "events", []):
            yield event
    recognizer.stop()
