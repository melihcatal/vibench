"""
Handles partial and final streaming recognition events using Deepgram Streaming API.

Manages the lifecycle of partial (interim) and final transcript events from
Deepgram's streaming speech-to-text service, providing deduplication, merging,
and state tracking for real-time transcription workflows.

Requires:
    pip install deepgram-sdk
"""

import asyncio
import time
from typing import AsyncIterator, List, Optional, Callable, Dict, Any

from deepgram import DeepgramClient, LiveOptions
from deepgram.audio.microphone.microphone import Microphone

from speech_client import build_deepgram_client
from speech_models import (
    TranscriptChunk,
    TranscriptStatus,
    StreamingTranscriptEvent,
    parse_deepgram_response,
    normalize_transcript_text,
)


class PartialResultHandler:
    """Handles partial and final streaming recognition events from Deepgram.

    Manages the state of interim and final transcripts, provides deduplication,
    and offers callbacks for transcript events.
    """

    def __init__(
        self,
        on_interim: Optional[Callable[[TranscriptChunk], None]] = None,
        on_final: Optional[Callable[[TranscriptChunk], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        self._interim_buffer: List[TranscriptChunk] = []
        self._final_results: List[TranscriptChunk] = []
        self._current_interim: Optional[TranscriptChunk] = None
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_error = on_error
        self._start_time = time.time()

    @property
    def full_transcript(self) -> str:
        """Get the full accumulated final transcript."""
        return " ".join(
            chunk.normalize_text()
            for chunk in self._final_results
            if chunk.text.strip()
        )

    @property
    def current_interim_text(self) -> str:
        """Get the current interim transcript text."""
        if self._current_interim:
            return self._current_interim.text
        return ""

    def handle_event(self, event: StreamingTranscriptEvent) -> Optional[TranscriptChunk]:
        """Process a streaming transcript event from Deepgram.

        Args:
            event: A StreamingTranscriptEvent from Deepgram.

        Returns:
            TranscriptChunk if the event was processed, None otherwise.
        """
        chunk = event.to_chunk()
        chunk.start_time = time.time() - self._start_time

        if event.is_final:
            self._finalize_interim(chunk)
            self._final_results.append(chunk)
            if self._on_final:
                self._on_final(chunk)
            return chunk
        else:
            self._current_interim = chunk
            self._interim_buffer.append(chunk)
            if self._on_interim:
                self._on_interim(chunk)
            return chunk

    def _finalize_interim(self, final_chunk: TranscriptChunk) -> None:
        """Replace the current interim transcript with a final one."""
        if self._current_interim:
            self._current_interim.status = TranscriptStatus.FINAL
            self._current_interim.is_final = True
            self._interim_buffer = []
        self._current_interim = None

    def get_results(self) -> Dict[str, Any]:
        """Get all collected results."""
        return {
            "final_transcript": self.full_transcript,
            "interim_text": self.current_interim_text,
            "final_count": len(self._final_results),
            "duration": time.time() - self._start_time,
        }


async def stream_with_partial_handling(
    audio_source,
    language: str = "en",
    model: str = "nova-2",
    sample_rate: int = 16000,
    handler: Optional[PartialResultHandler] = None,
    api_key: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    """Stream audio with partial result handling using Deepgram.

    Establishes a Deepgram streaming connection and processes results
    through a PartialResultHandler, yielding both interim and final chunks.

    Args:
        audio_source: Async iterable of audio chunks.
        language: Language code for transcription.
        model: Deepgram model identifier.
        sample_rate: Audio sample rate in Hz.
        handler: Optional PartialResultHandler for callbacks.
        api_key: Deepgram API key.

    Yields:
        TranscriptChunk objects as they are processed.
    """
    if handler is None:
        handler = PartialResultHandler()

    client = build_deepgram_client(api_key=api_key)

    live_options = LiveOptions(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=1,
        encoding="linear16",
        smart_format=True,
        interim_results=True,
        punctuate=True,
    )

    async with client.listen.live.v("1") as connection:
        send_task = asyncio.create_task(
            _send_audio_to_deepgram(connection, audio_source)
        )

        try:
            async for result in connection.results:
                raw_response = _result_to_dict(result)
                event = parse_deepgram_response(raw_response)
                chunk = handler.handle_event(event)
                if chunk:
                    yield chunk
        except Exception as e:
            if handler._on_error:
                handler._on_error(e)
            raise
        finally:
            send_task.cancel()
            try:
                await send_task
            except asyncio.CancelledError:
                pass


async def _send_audio_to_deepgram(connection, audio_source) -> None:
    """Send audio data from source to Deepgram connection."""
    try:
        async for chunk in audio_source:
            if isinstance(chunk, bytes):
                await connection.send(chunk)
            else:
                await connection.send(chunk.data)
    except Exception:
        pass
    finally:
        await connection.finish()


def _result_to_dict(result) -> Dict[str, Any]:
    """Convert a Deepgram SDK result object to a dictionary for parsing."""
    if hasattr(result, "to_dict"):
        return result.to_dict()

    response = {}
    response["is_final"] = getattr(result, "is_final", False)
    
    channel_data = {}
    if hasattr(result, "channel") and result.channel:
        alternatives = []
        if hasattr(result.channel, "alternatives"):
            for alt in result.channel.alternatives:
                alt_dict = {
                    "transcript": getattr(alt, "transcript", ""),
                    "confidence": getattr(alt, "confidence", 0.0),
                }
                if hasattr(alt, "words"):
                    alt_dict["words"] = [
                        {"word": w.word, "start": w.start, "end": w.end}
                        for w in alt.words
                    ] if alt.words else []
                alternatives.append(alt_dict)
        channel_data["alternatives"] = alternatives
    response["channel"] = channel_data

    metadata = {}
    if hasattr(result, "metadata") and result.metadata:
        metadata["model"] = getattr(result.metadata, "model", None)
        metadata["request_id"] = getattr(result.metadata, "request_id", None)
    response["metadata"] = metadata

    return response


if __name__ == "__main__":
    async def main():
        handler = PartialResultHandler(
            on_interim=lambda c: print(f"[INTERIM] {c.text}"),
            on_final=lambda c: print(f"[FINAL] {c.text}"),
        )

        async def dummy_audio():
            yield b"\x00" * 4096

        async for chunk in stream_with_partial_handling(
            audio_source=dummy_audio(),
            handler=handler,
        ):
            pass

        results = handler.get_results()
        print(f"\nFull transcript: {results['final_transcript']}")

    asyncio.run(main())
