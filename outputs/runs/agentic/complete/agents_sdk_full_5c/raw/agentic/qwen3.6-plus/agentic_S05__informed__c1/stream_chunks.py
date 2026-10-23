"""
Streams audio chunks from an async source using Deepgram Streaming API.

Accepts audio chunks from any async iterable source (file, network stream,
generator, etc.) and streams them to Deepgram for real-time transcription,
yielding interim and final transcript results.

Requires:
    pip install deepgram-sdk
"""

import asyncio
from typing import AsyncIterable, AsyncIterator, Optional, Union

from deepgram import DeepgramClient, LiveOptions

from speech_client import build_deepgram_client
from speech_models import TranscriptChunk, TranscriptStatus, AudioChunk


async def stream_audio_chunks(
    audio_source: Union[AsyncIterable[bytes], AsyncIterable[AudioChunk]],
    language: str = "en",
    model: str = "nova-2",
    sample_rate: int = 16000,
    channels: int = 1,
    interim_results: bool = True,
    punctuate: bool = True,
    smart_format: bool = True,
    api_key: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    """Stream audio chunks from an async source to Deepgram and yield transcripts.

    Connects to the Deepgram streaming WebSocket API and sends audio chunks
    from the provided async source. Yields TranscriptChunk objects as interim
    and final transcription results arrive.

    Args:
        audio_source: Async iterable yielding bytes or AudioChunk objects.
        language: Language code for transcription (e.g., 'en', 'es', 'ja').
        model: Deepgram model identifier (e.g., 'nova-2', 'nova-2-general').
        sample_rate: Audio sample rate in Hz.
        channels: Number of audio channels.
        interim_results: Whether to yield interim (partial) transcripts.
        punctuate: Whether to add punctuation to transcripts.
        smart_format: Enable Deepgram smart formatting.
        api_key: Deepgram API key. Falls back to DEEPGRAM_API_KEY env var.

    Yields:
        TranscriptChunk objects with transcribed text and metadata.
    """
    client = build_deepgram_client(api_key=api_key)

    live_options = LiveOptions(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        encoding="linear16",
        smart_format=smart_format,
        interim_results=interim_results,
        punctuate=punctuate,
    )

    async with client.listen.live.v("1") as connection:
        send_task = asyncio.create_task(
            _send_chunks(connection, audio_source)
        )

        async for result in connection.results:
            transcript = _parse_deepgram_result(result)
            if transcript is not None:
                yield transcript

        await send_task


async def _send_chunks(
    connection,
    audio_source: Union[AsyncIterable[bytes], AsyncIterable[AudioChunk]],
) -> None:
    """Send audio chunks from the async source to the Deepgram connection."""
    try:
        async for chunk in audio_source:
            if isinstance(chunk, AudioChunk):
                if chunk.is_end:
                    await connection.finish()
                    return
                await connection.send(chunk.data)
            else:
                await connection.send(chunk)
    except Exception:
        pass
    finally:
        await connection.finish()


def _parse_deepgram_result(result) -> Optional[TranscriptChunk]:
    """Parse a Deepgram streaming result into a TranscriptChunk."""
    if not hasattr(result, "channel") or result.channel is None:
        return None

    alternatives = getattr(result.channel, "alternatives", [])
    if not alternatives:
        return None

    alternative = alternatives[0]
    transcript_text = getattr(alternative, "transcript", "").strip()
    confidence = getattr(alternative, "confidence", 0.0)

    if not transcript_text:
        return None

    is_final = getattr(result, "is_final", False)

    return TranscriptChunk(
        text=transcript_text,
        status=TranscriptStatus.FINAL if is_final else TranscriptStatus.INTERIM,
        confidence=confidence,
        is_final=is_final,
    )


async def stream_file_chunks(
    file_path: str,
    chunk_size: int = 4096,
    **kwargs,
) -> AsyncIterator[TranscriptChunk]:
    """Stream audio from a file as chunks to Deepgram.

    Args:
        file_path: Path to the audio file.
        chunk_size: Size of each audio chunk in bytes.
        **kwargs: Additional arguments passed to stream_audio_chunks.

    Yields:
        TranscriptChunk objects from the file transcription.
    """

    async def file_generator():
        with open(file_path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    async for chunk in stream_audio_chunks(file_generator(), **kwargs):
        yield chunk


if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python stream_chunks.py <audio_file_path>")
            return

        file_path = sys.argv[1]
        async for chunk in stream_file_chunks(file_path):
            prefix = "[FINAL]" if chunk.is_final else "[INTERIM]"
            print(f"{prefix} {chunk.text}")

    asyncio.run(main())
