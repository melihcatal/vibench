from __future__ import annotations

from typing import AsyncIterator, Optional

from deepgram import LiveTranscriptionEvents

from speech_client import DeepgramSpeechService
from speech_models import AudioChunk, StreamingSpeechConfig, TranscriptSegment


async def stream_chunks(source: AsyncIterator[AudioChunk], language_code: str = "en-US") -> AsyncIterator[TranscriptSegment]:
    service = DeepgramSpeechService()
    options = service.live_options(
        StreamingSpeechConfig(language_code=language_code, enable_punctuation=True, interim_results=True)
    )
    raise NotImplementedError("Adapt async audio chunks to Deepgram's live transcription stream.")
