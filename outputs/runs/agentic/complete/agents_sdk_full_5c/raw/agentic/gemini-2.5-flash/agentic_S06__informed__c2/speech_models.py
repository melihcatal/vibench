from typing import Literal, Optional
from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0

    def __post_init__(self):
        if not self.text and not self.ssml:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if self.text and self.ssml:
            raise ValueError("Cannot provide both 'text' and 'ssml'.")

@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"]

@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    ssml_gender: Literal["MALE", "FEMALE", "NEUTRAL", "UNSPECIFIED"]
    natural_sample_rate_hertz: int


if __name__ == '__main__':
    # Example usage of the data models
    req_text = SynthesisRequest(text="Hello, world.", voice_name="en-US-Standard-A")
    print(f"Text Request: {req_text}")

    req_ssml = SynthesisRequest(ssml="<speak>Hello.</speak>", audio_encoding="LINEAR16")
    print(f"SSML Request: {req_ssml}")

    # Example of a voice info
    voice = VoiceInfo(name="en-US-Wavenet-F", language_codes=["en-US"], ssml_gender="FEMALE", natural_sample_rate_hertz=24000)
    print(f"Voice Info: {voice}")

    try:
        SynthesisRequest() # This should raise a ValueError
    except ValueError as e:
        print(f"Expected error: {e}")
