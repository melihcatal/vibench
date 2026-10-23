from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, AsyncIterable, Iterable, Optional

from deepgram import DeepgramClient, LiveOptions, Microphone, SpeakOptions

from speech_models import StreamConfig, StreamResult, TranscriptChunk, normalize_transcript_text


DEEPGRAM_API_KEY_ENV = "DEEPGRAM_API_KEY"
DEFAULT_DEEPGRAM_MODEL = "nova-2"


def load_stream_config() -> StreamConfig:
    return StreamConfig(
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        enable_automatic_punctuation=os.getenv("SPEECH_PUNCTUATION", "true").lower() == "true",
        interim_results=os.getenv("SPEECH_INTERIM_RESULTS", "true").lower() == "true",
        sample_rate_hz=int(os.getenv("SPEECH_SAMPLE_RATE_HZ", "16000")),
        encoding=os.getenv("SPEECH_ENCODING", "linear16"),
        model=os.getenv("DEEPGRAM_MODEL", DEFAULT_DEEPGRAM_MODEL),
    )


def build_deepgram_client() -> DeepgramClient:
    api_key = os.environ[DEEPGRAM_API_KEY_ENV]
    return DeepgramClient(api_key)


def build_live_options(config: StreamConfig) -> LiveOptions:
    return LiveOptions(
        model=config.model,
        language=config.language_code,
        punctuate=config.enable_automatic_punctuation,
        interim_results=config.interim_results,
        encoding=config.encoding,
        sample_rate=config.sample_rate_hz,
    )


def transcript_chunk_from_event(event: Any) -> TranscriptChunk:
    channel = getattr(event, "channel", None)
    alternatives = getattr(channel, "alternatives", None) or []
    transcript = ""
    confidence = None
    if alternatives:
        top = alternatives[0]
        transcript = normalize_transcript_text(getattr(top, "transcript", "") or "")
        confidence = getattr(top, "confidence", None)
    is_final = bool(getattr(event, "is_final", False))
    language = getattr(event, "language", None)
    return TranscriptChunk(
        text=transcript,
        is_final=is_final,
        confidence=confidence,
        language=language,
        raw=event,
    )


async def stream_async_chunks(client: DeepgramClient, chunks: AsyncIterable[bytes], config: Optional[StreamConfig] = None) -> StreamResult:
    config = config or load_stream_config()
    options = build_live_options(config)
    result = StreamResult()
    conn = await client.listen.asyncwebsocket.v("1")
    await conn.start(options)
    async for chunk in chunks:
        await conn.send(chunk)
    await conn.finish()
    return result


def microphone_stream(client: Optional[DeepgramClient] = None) -> Microphone:
    client = client or build_deepgram_client()
    return Microphone(client)
