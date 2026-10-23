"""
Stream microphone audio and yield interim transcripts using Google Cloud Speech-to-Text.

This module captures audio from the system microphone and streams it to the
Google Cloud Speech-to-Text API (hostname: speech.googleapis.com) using the
cloud-speech library. Interim (partial) transcripts are yielded as they become
available during the streaming recognition session.
"""

import asyncio
import logging
from typing import AsyncIterator

from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
    StreamingRecognizeResponse,
)

logger = logging.getLogger(__name__)

GOOGLE_CLOUD_SPEECH_API_ENDPOINT = "speech.googleapis.com"
GOOGLE_SPEECH_MODEL_ID = "latest_long"


def create_streaming_config(
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: str = GOOGLE_SPEECH_MODEL_ID,
) -> StreamingRecognitionConfig:
    """Create a Google Cloud Speech-to-Text streaming recognition configuration."""
    config = RecognitionConfig(
        model=model,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        max_alternatives=1,
    )
    return StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        streaming_features=StreamingRecognitionConfig.StreamingFeatures(
            voice_activity_events=True,
        ),
    )


async def stream_microphone_audio(
    sample_rate_hertz: int = 16000,
    chunk_duration_ms: int = 500,
    buffer_size: int = 8192,
) -> AsyncIterator[dict]:
    """
    Stream audio from the microphone and yield interim transcript results.

    Yields:
        dict: Interim transcript data with keys:
            - 'text': recognized text (str)
            - 'is_final': whether this is a final result (bool)
            - 'confidence': recognition confidence (float, 0-1)
            - 'stability': result stability score (float, 0-1)
    """
    import sounddevice as sd
    import queue

    audio_queue = queue.Queue()
    stop_event = asyncio.Event()

    def audio_callback(indata, frames, time_info, status):
        if status:
            logger.warning("Microphone status: %s", status)
        audio_queue.put(bytes(indata))

    speech_client = SpeechClient()

    streaming_config = create_streaming_config(
        sample_rate_hertz=sample_rate_hertz,
    )

    async def audio_generator():
        yield StreamingRecognizeRequest(
            streaming_config=streaming_config
        )
        while not stop_event.is_set():
            try:
                audio_chunk = audio_queue.get(timeout=0.1)
                yield StreamingRecognizeRequest(audio_content=audio_chunk)
            except queue.Empty:
                continue

    with sd.InputStream(
        samplerate=sample_rate_hertz,
        channels=1,
        dtype="int16",
        blocksize=int(sample_rate_hertz * chunk_duration_ms / 1000),
        callback=audio_callback,
    ):
        logger.info(
            "Streaming microphone audio to Google Cloud Speech-to-Text at %s",
            GOOGLE_CLOUD_SPEECH_API_ENDPOINT,
        )

        responses: AsyncIterator[StreamingRecognizeResponse] = (
            speech_client.streaming_recognize(requests=audio_generator())
        )

        async for response in responses:
            for result in response.results:
                if not result.alternatives:
                    continue

                best_alternative = result.alternatives[0]
                transcript_data = {
                    "text": best_alternative.transcript,
                    "is_final": result.is_final,
                    "confidence": best_alternative.confidence,
                    "stability": result.stability,
                }

                if not result.is_final:
                    logger.debug("Interim transcript: %s", transcript_data["text"])
                else:
                    logger.info("Final transcript: %s", transcript_data["text"])

                yield transcript_data

    stop_event.set()
