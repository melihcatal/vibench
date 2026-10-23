from typing import List, Optional
from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str
    voice_name: str
    language_code: str
    ssml: bool = False
    audio_encoding: str = "MP3"

@dataclass
class SynthesisResponse:
    audio_content: bytes
    mime_type: str = "audio/mpeg" # Default for MP3

@dataclass
class Voice:
    name: str
    language_codes: List[str]
    gender: str
    natural_sample_rate_hertz: Optional[int] = None

@dataclass
class VoiceSelection:
    language_code: str
    gender: Optional[str] = None
    name: Optional[str] = None

if __name__ == "__main__":
    # Example usage
    request = SynthesisRequest(
        text="Hello world",
        voice_name="en-US-Standard-A",
        language_code="en-US"
    )
    print(request)

    dummy_audio = b"dummy_audio_bytes"
    response = SynthesisResponse(audio_content=dummy_audio)
    print(response)

    voice = Voice(name="en-US-Wavenet-A", language_codes=["en-US"], gender="FEMALE")
    print(voice)
