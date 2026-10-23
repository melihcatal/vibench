import base64
from dataclasses import dataclass


def normalize_language_code(value, default="en-US"):
    return (value or default).replace("_", "-")


def normalize_text(value):
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def decode_audio_chunk(chunk):
    if chunk is None:
        return b""
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, str):
        try:
            return base64.b64decode(chunk)
        except Exception:
            return chunk.encode()
    return bytes(chunk)


@dataclass
class StreamingSpeechConfig:
    region: str = "us-east-1"
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    media_encoding: str = "pcm"
    enable_partial_results_stabilization: bool = True
    show_speaker_label: bool = False
    enable_punctuation: bool = True


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
