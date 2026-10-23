import os
from typing import Literal, TypedDict, List, Optional

# Provider choices already defined in speech_client.py
PROVIDER_NAME: Literal["Google Cloud Text-to-Speech"] = "Google Cloud Text-to-Speech"

# ---------------------------------------------------------------------------
# Request & response type models
# ---------------------------------------------------------------------------


class VoiceInfo(TypedDict):
    name: str
    language_codes: List[str]
    ssml_gender: Literal["MALE", "FEMALE", "NEUTRAL"]
    natural_sample_rate_hertz: int


class SynthesisRequest(TypedDict):
    input_text: Optional[str]
    input_ssml: Optional[str]
    voice_name: Optional[str]
    language_code: str
    voice_gender: Optional[str]
    prosody: Optional[dict]  # e.g., {"rate": 0.9}
    audio_encoding: str = "MP3"


class SynthesisResponse(TypedDict):
    audio_content: bytes
    metadata: Optional[dict]


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def normalize_request(params: SynthesisRequest) -> dict:
    """Convert arbitrary user input to the concrete provider model.

    Returns a dict compatible with Google Cloud Text-to-Speech SDK.
    """
    from google.cloud import texttospeech

    input_ = params.get("input_text") or params.get("input_ssml")
    if not input_:
        raise ValueError(
            "Synthesis request must provide either input_text or input_ssml"
        )
    norm = {
        "input": input_,
        "voice_name": params.get("voice_name"),
        "language_code": params.get("language_code", "en-US"),
        "audio_encoding": params.get("audio_encoding", "MP3"),
    }
    # Gender handling (maps user-friendly string to SDK enum)
    gender = params.get("voice_gender")
    if gender:
        gender_map = {
            "MALE": texttospeech.SsmlVoiceGender.MALE,
            "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
            "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
        }
        norm["voice_gender"] = gender_map.get(
            gender.upper(), texttospeech.SsmlVoiceGender.UNSPECIFIED
        )
    # Prosody – simple flat mapping for demo (expand as needed)
    norm["prosody"] = params.get("prosody")
    return norm


def normalize_response(response: SynthesisResponse) -> bytes:
    """Extract raw audio bytes from provider response.

    Provider-specific conversion should be done in the client layer; here we just return the payload.
    """
    return response["audio_content"]
