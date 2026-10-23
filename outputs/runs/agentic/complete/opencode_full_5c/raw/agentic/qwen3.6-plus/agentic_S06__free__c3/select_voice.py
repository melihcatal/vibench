import os
from speech_client import get_openai_client
from speech_models import VoiceInfo


OPENAI_VOICES = [
    VoiceInfo(
        id="alloy", locale="en-US", gender="neutral", description="Balanced and clear"
    ),
    VoiceInfo(
        id="echo", locale="en-US", gender="male", description="Deep and resonant"
    ),
    VoiceInfo(
        id="fable", locale="en-GB", gender="male", description="British, warm tone"
    ),
    VoiceInfo(
        id="onyx", locale="en-US", gender="male", description="Authoritative and strong"
    ),
    VoiceInfo(
        id="nova", locale="en-US", gender="female", description="Friendly and warm"
    ),
    VoiceInfo(
        id="shimmer", locale="en-US", gender="female", description="Light and gentle"
    ),
]


def list_vvoices() -> list[VoiceInfo]:
    return list(OPENAI_VOICES)


def select_voice(
    locale: str = "en-US",
    gender: str | None = None,
    model: str = "tts-1",
) -> VoiceInfo:
    client = get_openai_client()
    candidates = [v for v in OPENAI_VOICES if v.locale.lower() == locale.lower()]
    if gender:
        candidates = [v for v in candidates if v.gender == gender]
    if not candidates:
        candidates = OPENAI_VOICES
    selected = candidates[0]
    return selected
