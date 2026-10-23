from dataclasses import dataclass
from typing import Optional

# Although Google Cloud TTS SDK types are rich, these serve as local helper models
# for request/response normalization if custom structures were needed.

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-C"
    audio_encoding: str = "MP3" # Corresponds to google.cloud.texttospeech.AudioEncoding

@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_encoding: str

@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    ssml_gender: str
    natural_sample_rate_hertz: int

if __name__ == "__main__":
    # Example usage
    req = SynthesisRequest(text="Hello from models!")
    print(f"Synthesis Request: {req.text}, {req.language_code}")

    audio_bytes = b"\x00\x01\x02"
    resp = SynthesisResponse(audio_content=audio_bytes, audio_encoding="MP3")
    print(f"Synthesis Response: {len(resp.audio_content)} bytes, {resp.audio_encoding}")

    voice = VoiceInfo(
        name="en-US-Standard-C",
        language_codes=["en-US"],
        ssml_gender="FEMALE",
        natural_sample_rate_hertz=24000
    )
    print(f"Voice Info: {voice.name}, {voice.ssml_gender}")
