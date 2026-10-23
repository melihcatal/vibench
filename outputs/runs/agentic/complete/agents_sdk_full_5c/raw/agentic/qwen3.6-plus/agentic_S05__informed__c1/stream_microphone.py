"""
Streams microphone audio and yields interim transcripts using Deepgram Streaming API.

Captures real-time audio from the system microphone, streams it to Deepgram's
WebSocket-based streaming transcription endpoint, and yields interim and final
transcripts as they become available.

Requires:
    pip install deepgram-sdk pyaudio
"""

import asyncio
import queue
import threading
from typing import AsyncGenerator, Optional

from deepgram import DeepgramClient, LiveOptions
import pyaudio

from speech_client import build_deepgram_client, get_default_streaming_options
from speech_models import SpeechConfig, TranscriptChunk, TranscriptStatus


AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
CHUNK_SIZE = 4096


class MicrophoneStream:
    """Manages microphone audio capture using PyAudio."""

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
        chunk_size: int = CHUNK_SIZE,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self._audio = pyaudio.PyAudio()
        self._stream = None
        self._running = False
        self._buffer = queue.Queue()

    def open(self) -> None:
        """Open the microphone audio stream."""
        self._stream = self._audio.open(
            format=AUDIO_FORMAT,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback,
        )
        self._running = True

    def _audio_callback(self, in_data, frame_count, time_info, status) -> tuple:
        """PyAudio callback to buffer incoming audio data."""
        if self._running:
            self._buffer.put(in_data)
        return (None, pyaudio.paContinue)

    def read(self) -> bytes:
        """Read the next audio chunk from the buffer."""
        return self._buffer.get()

    def close(self) -> None:
        """Close the microphone audio stream."""
        self._running = False
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        self._audio.terminate()


async def stream_microphone_transcripts(
    language: str = "en",
    model: str = "nova-2",
    sample_rate: int = SAMPLE_RATE,
    interim_results: bool = True,
    punctuate: bool = True,
    api_key: Optional[str] = None,
) -> AsyncGenerator[TranscriptChunk, None]:
    """Stream microphone audio to Deepgram and yield interim/final transcripts.

    Uses the Deepgram SDK to establish a WebSocket streaming connection,
    captures audio from the system microphone via PyAudio, and yields
    TranscriptChunk objects as interim and final results arrive.

    Args:
        language: Language code for transcription (e.g., 'en', 'es', 'fr').
        model: Deepgram model identifier (e.g., 'nova-2', 'nova-2-general').
        sample_rate: Audio sample rate in Hz.
        interim_results: Whether to yield interim (partial) transcripts.
        punctuate: Whether to add punctuation to transcripts.
        api_key: Deepgram API key. Falls back to DEEPGRAM_API_KEY env var.

    Yields:
        TranscriptChunk objects containing transcribed text and status.
    """
    client = build_deepgram_client(api_key=api_key)

    live_options = LiveOptions(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=CHANNELS,
        encoding="linear16",
        smart_format=True,
        interim_results=interim_results,
        punctuate=punctuate,
    )

    microphone = MicrophoneStream(sample_rate=sample_rate)
    microphone.open()

    try:
        async with client.listen.live.v("1") as connection:
            async def send_audio():
                """Background task to send microphone audio to Deepgram."""
                while microphone._running:
                    try:
                        audio_data = microphone.read()
                        await connection.send(audio_data)
                    except Exception:
                        break
                await connection.finish()

            send_task = asyncio.create_task(send_audio())

            async for result in connection.results:
                if result.is_final:
                    transcript_text = result.channel.alternatives[0].transcript
                    confidence = result.channel.alternatives[0].confidence
                    yield TranscriptChunk(
                        text=transcript_text,
                        status=TranscriptStatus.FINAL,
                        confidence=confidence,
                        is_final=True,
                    )
                elif interim_results:
                    transcript_text = result.channel.alternatives[0].transcript
                    if transcript_text.strip():
                        confidence = result.channel.alternatives[0].confidence
                        yield TranscriptChunk(
                            text=transcript_text,
                            status=TranscriptStatus.INTERIM,
                            confidence=confidence,
                            is_final=False,
                        )

            send_task.cancel()
            try:
                await send_task
            except asyncio.CancelledError:
                pass

    finally:
        microphone.close()


if __name__ == "__main__":
    async def main():
        async for chunk in stream_microphone_transcripts():
            prefix = "[FINAL]" if chunk.is_final else "[INTERIM]"
            print(f"{prefix} {chunk.text} (confidence: {chunk.confidence:.2f})")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped streaming.")
