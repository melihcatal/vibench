from __future__ import annotations

from typing import Iterator, Optional

from deepgram import LiveTranscriptionEvents

from speech_client import DeepgramSpeechService
from speech_models import StreamingSpeechConfig, TranscriptSegment


def stream_microphone(language_code: str = "en-US") -> Iterator[TranscriptSegment]:
    service = DeepgramSpeechService()
    options = service.live_options(
        StreamingSpeechConfig(language_code=language_code, enable_punctuation=True, interim_results=True)
    )
    raise NotImplementedError("Connect microphone audio to Deepgram LiveTranscriptionEvents using the Deepgram SDK.")
