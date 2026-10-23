from __future__ import annotations

import asyncio
import os
from typing import AsyncIterable, AsyncIterator, Iterable

from google.cloud import speech

from speech_models import StreamChunk, StreamingConfig


GOOGLE_SPEECH_MODEL = "latest_long"
GOOGLE_RECOGNIZER_PROVIDER = "google-cloud-speech"



def get_speech_client() -> speech.SpeechClient:
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return speech.SpeechClient()



def build_streaming_config(config: StreamingConfig) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, config.encoding),
        sample_rate_hertz=config.sample_rate_hz,
        language_code=config.language_code,
        audio_channel_count=config.channels,
        enable_automatic_punctuation=config.punctuation,
        model=config.model or GOOGLE_SPEECH_MODEL,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=config.interim_results,
        single_utterance=False,
    )



def request_iter_from_chunks(chunks: Iterable[bytes]) -> Iterable[speech.StreamingRecognizeRequest]:
    for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)


async def async_request_iter_from_source(
    source: AsyncIterable[bytes | StreamChunk],
) -> AsyncIterator[speech.StreamingRecognizeRequest]:
    async for item in source:
        if isinstance(item, StreamChunk):
            payload = item.audio
        else:
            payload = item
        if payload:
            yield speech.StreamingRecognizeRequest(audio_content=payload)
        await asyncio.sleep(0)
