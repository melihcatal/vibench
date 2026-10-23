from typing import TypedDict, Optional, Union

class VoiceSelectionParams(TypedDict):
    language_code: str
    name: Optional[str]
    ssml_gender: Optional[str]

class AudioConfig(TypedDict):
    audio_encoding: str
    speaking_rate: Optional[float]
    pitch: Optional[float]
    volume_gain_db: Optional[float]

class SynthesisInput(TypedDict):
    text: Optional[str]
    ssml: Optional[str]

# Normalization helpers
def normalize_audio_encoding(encoding: str) -> str:
    """Normalize audio encoding name."""
    encodings = {
        "mp3": "MP3",
        "ogg": "OGG_OPUS",
        "linear16": "LINEAR16",
    }
    return encodings.get(encoding.lower(), "MP3")
