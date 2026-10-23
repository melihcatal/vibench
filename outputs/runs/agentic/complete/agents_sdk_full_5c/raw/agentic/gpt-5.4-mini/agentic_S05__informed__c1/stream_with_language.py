from __future__ import annotations

from deepgram import LiveTranscriptionEvents

from speech_client import DeepgramSpeechService
from speech_models import StreamingSpeechConfig


def stream_with_language(language_code: str = "es-ES", punctuation: bool = True) -> None:
    service = DeepgramSpeechService()
    options = service.live_options(
        StreamingSpeechConfig(language_code=language_code, enable_punctuation=punctuation, interim_results=True)
    )
    raise NotImplementedError("Use Deepgram live transcription with the configured language and punctuation options.")
