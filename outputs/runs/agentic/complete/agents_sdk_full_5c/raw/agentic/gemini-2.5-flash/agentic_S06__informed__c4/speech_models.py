from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class TTSRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Standard-W"
    language_code: str = "en-US"
    audio_encoding: str = "MP3"

@dataclass
class TTSResponse:
    audio_content: bytes
    encoding: str

@dataclass
class VoiceInfo:
    name: str
    ssml_gender: str
    natural_sample_rate_hertz: int
    language_codes: List[str]


def normalize_voice_info(google_voice_obj: Any) -> VoiceInfo:
    """Normalizes a Google Cloud Text-to-Speech Voice object to a local VoiceInfo dataclass."""
    from google.cloud import texttospeech # Import here to avoid circular dependency if texttospeech is used in client

    return VoiceInfo(
        name=google_voice_obj.name,
        ssml_gender=texttospeech.SsmlVoiceGender(google_voice_obj.ssml_gender).name,
        natural_sample_rate_hertz=google_voice_obj.natural_sample_rate_hertz,
        language_codes=list(google_voice_obj.language_codes)
    )


if __name__ == '__main__':
    # Example usage (requires google.cloud.texttospeech for normalization example):
    # from google.cloud import texttospeech
    # dummy_google_voice = texttospeech.Voice(
    #     name="en-US-Wavenet-A",
    #     ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    #     natural_sample_rate_hertz=24000,
    #     language_codes=["en-US"]
    # )
    # normalized_voice = normalize_voice_info(dummy_google_voice)
    # print(normalized_voice)
    pass
