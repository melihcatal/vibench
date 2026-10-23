from typing import NamedTuple, Optional
from enum import Enum

class AudioFormat(Enum):
    MP3 = "mp3"
    LINEAR16 = "linear16"
    OGG_OPUS = "ogg_opus"

class VoiceGender(Enum):
    UNSPECIFIED = "unspecified"
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class SynthesisRequest(NamedTuple):
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Wavenet-C"
    language_code: str = "en-US"
    audio_format: AudioFormat = AudioFormat.MP3

class Voice(NamedTuple):
    name: str
    language_codes: list[str]
    gender: VoiceGender
    natural_sample_rate_hertz: int

if __name__ == "__main__":
    # Example usage of the models
    req_text = SynthesisRequest(text="Hello world")
    req_ssml = SynthesisRequest(ssml="<speak>Hello <break time=\"1s\"/>world</speak>", audio_format=AudioFormat.OGG_OPUS)
    print(f"Text request: {req_text}")
    print(f"SSML request: {req_ssml}")

    example_voice = Voice(
        name="en-US-Wavenet-C",
        language_codes=["en-US"],
        gender=VoiceGender.MALE,
        natural_sample_rate_hertz=24000
    )
    print(f"Example voice: {example_voice}")
