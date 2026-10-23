"""
Stream audio chunks from an async source to Google Cloud Speech-to-Text.

Consumes audio data from an async iterator source (e.g., WebSocket, async file read,
network stream) and streams the chunks to Google Cloud Speech-to-Text for recognition.

Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import asyncio
import queue
import threading
from typing import AsyncGenerator, AsyncIterator, Optional

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_client import create_streaming_speech_client, build_streaming_config
from speech_models import extract_interim_transcript, extract_final_transcripts


async def stream_audio_chunks(
    audio_source: AsyncIterator[bytes],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_punctuation: bool = True,
    encoding: speech_types.RecognitionConfig.AudioEncoding = speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
    chunk_size: int = 6400,
) -> AsyncGenerator[dict, None]:
    """
    Stream audio chunks from an async source to Google Cloud Speech-to-Text.

    Reads audio data from the provided async iterator, buffers chunks to meet
    the minimum size requirements, and streams them to the Google Cloud Speech
    streaming recognition API. Yields interim and final transcription results.

    Args:
        audio_source: Async iterator yielding raw audio bytes.
        language_code: BCP-47 language code for recognition.
        sample_rate_hertz: Audio sample rate in Hz.
        enable_punctuation: Whether to enable automatic punctuation.
        encoding: Audio encoding format.
        chunk_size: Minimum byte size for each streamed chunk.

    Yields:
        Dict with keys:
            - 'type': 'interim' or 'final'
            - 'text': Transcribed text
            - 'confidence': Confidence score (0.0-1.0)
    """
    config = build_streaming_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        encoding=encoding,
        enable_automatic_punctuation=enable_punctuation,
        interim_results=True,
    )

    client = create_streaming_speech_client()
    chunk_queue: queue.Queue = queue.Queue()
    done_event = threading.Event()
    error_holder: dict = {"exception": None}

    async def _feed_chunks():
        """Async task that reads from audio_source and feeds into the sync queue."""
        buffer = b""
        try:
            async for chunk in audio_source:
                buffer += chunk
                while len(buffer) >= chunk_size:
                    chunk_queue.put(buffer[:chunk_size])
                    buffer = buffer[chunk_size:]
            if buffer:
                chunk_queue.put(buffer)
        except Exception as e:
            error_holder["exception"] = e
        finally:
            chunk_queue.put(None)
            done_event.set()

    feed_task = asyncio.create_task(_feed_chunks())

    try:
        responses = client.streaming_recognize(
            config=_streaming_request_generator(config, chunk_queue, done_event)
        )

        for response in responses:
            interim_text = extract_interim_transcript(response)
            if interim_text:
                yield {
                    "type": "interim",
                    "text": interim_text,
                    "confidence": 0.0,
                }

            final_texts = extract_final_transcripts(response)
            for final_text in final_texts:
                for result in response.results:
                    if result.is_final and result.alternatives:
                        yield {
                            "type": "final",
                            "text": final_text,
                            "confidence": result.alternatives[0].confidence,
                        }
                        break

    except Exception as e:
        yield {
            "type": "error",
            "text": "",
            "confidence": 0.0,
            "error": str(e),
        }
    finally:
        if not done_event.is_set():
            done_event.set()
            chunk_queue.put(None)
        await feed_task


def _streaming_request_generator(
    config: speech_types.StreamingRecognitionConfig,
    chunk_queue: queue.Queue,
    done_event: threading.Event,
):
    """
    Generator that yields streaming recognition requests from a queue.

    Args:
        config: Pre-built streaming recognition config.
        chunk_queue: Queue containing audio byte chunks.
        done_event: Event signaled when no more audio will arrive.

    Yields:
        StreamingRecognizeRequest objects.
    """
    yield speech_types.StreamingRecognizeRequest(streaming_config=config)

    while True:
        try:
            chunk = chunk_queue.get(timeout=5.0)
            if chunk is None:
                break
            yield speech_types.StreamingRecognizeRequest(audio_content=chunk)
        except queue.Empty:
            if done_event.is_set():
                remaining = []
                while True:
                    try:
                        chunk = chunk_queue.get_nowait()
                        if chunk is None:
                            break
                        remaining.append(chunk)
                    except queue.Empty:
                        break
                for c in remaining:
                    yield speech_types.StreamingRecognizeRequest(audio_content=c)
                break
