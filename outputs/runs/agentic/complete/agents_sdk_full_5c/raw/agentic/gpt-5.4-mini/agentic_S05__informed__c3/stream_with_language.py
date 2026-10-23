from __future__ import annotations

from speech_client import AzureSpeechStreamingClient, SpeechConfig
from speech_models import StreamingTranscriptEvent


def stream_with_language(language_code: str = "en-US", enable_punctuation: bool = True) -> AzureSpeechStreamingClient:
    config = SpeechConfig(
        key=__import__("os").environ.get("AZURE_SPEECH_KEY", ""),
        region=__import__("os").environ.get("AZURE_SPEECH_REGION", ""),
        language=language_code,
        enable_punctuation=enable_punctuation,
    )
    return AzureSpeechStreamingClient(config=config)


def set_language_on_event(event: StreamingTranscriptEvent, language_code: str) -> StreamingTranscriptEvent:
    event.language_code = language_code
    return event
