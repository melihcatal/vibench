from __future__ import annotations

from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import AzureSpeechStreamingClient
from speech_models import StreamingConfig, TranscriptChunk


def stream_with_language(language_code: str = "en-US", enable_punctuation: bool = True) -> Iterator[TranscriptChunk]:
    client = AzureSpeechStreamingClient()
    cfg = StreamingConfig(language_code=language_code, enable_punctuation=enable_punctuation)
    recognizer = client.recognizer(cfg)
    recognizer.recognizing.connect(
        lambda evt: None
    )
    recognizer.start_continuous_recognition_async().get()
    yield TranscriptChunk(
        text=f"streaming started for {cfg.language_code} with punctuation={cfg.enable_punctuation}",
        is_final=False,
        metadata={"provider": "azure-speech", "language_code": cfg.language_code},
    )
    recognizer.stop_continuous_recognition_async().get()
