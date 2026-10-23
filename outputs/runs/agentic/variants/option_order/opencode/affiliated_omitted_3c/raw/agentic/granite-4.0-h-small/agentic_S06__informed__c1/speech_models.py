from typing import TypedDict, Literal


class SynthesizeRequest(TypedDict):
    """Request model for text-to-speech synthesis."""

    text: str
    ssml: str | None = None
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    audio_encoding: Literal["MP3", "WAV"] = "MP3"


class SynthesizeResponse(TypedDict):
    """Response model containing the audio bytes."""

    audio_content: bytes


def normalize_input(req: SynthesizeRequest) -> SynthesizeRequest:
    """Ensure only one of text or ssml is provided and set defaults."""
    if req.get("ssml") is None:
        req["ssml"] = ""
    if req.get("audio_encoding") == "WAV":
        req["audio_encoding"] = "WAV"
    return req
