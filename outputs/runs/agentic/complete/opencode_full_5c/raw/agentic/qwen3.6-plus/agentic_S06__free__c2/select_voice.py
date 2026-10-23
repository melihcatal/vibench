from typing import List, Optional
from speech_client import get_openai_client, DEFAULT_VOICES
from speech_models import VoiceInfo, VoiceSelectionRequest


OPENAI_VOICE_METADATA = {
    "alloy": {"name": "Alloy", "locale": "en-US", "gender": "neutral"},
    "echo": {"name": "Echo", "locale": "en-US", "gender": "male"},
    "fable": {"name": "Fable", "locale": "en-GB", "gender": "male"},
    "onyx": {"name": "Onyx", "locale": "en-US", "gender": "male"},
    "nova": {"name": "Nova", "locale": "en-US", "gender": "female"},
    "shimmer": {"name": "Shimmer", "locale": "en-US", "gender": "female"},
}


def list_vvoices() -> List[VoiceInfo]:
    voices = []
    for voice_id in DEFAULT_VOICES:
        meta = OPENAI_VOICE_METADATA.get(voice_id, {})
        voices.append(
            VoiceInfo(
                voice_id=voice_id,
                name=meta.get("name", voice_id),
                locale=meta.get("locale", "en-US"),
                gender=meta.get("gender", "unknown"),
            )
        )
    return voices


def select_voice(
    locale: str, gender: Optional[str] = None, voice_name: Optional[str] = None
) -> VoiceInfo:
    client = get_openai_client()

    if voice_name:
        if voice_name in OPENAI_VOICE_METADATA:
            meta = OPENAI_VOICE_METADATA[voice_name]
            return VoiceInfo(
                voice_id=voice_name,
                name=meta["name"],
                locale=meta["locale"],
                gender=meta["gender"],
            )
        raise ValueError(
            f"OpenAI voice '{voice_name}' not found. Available: {list(OPENAI_VOICE_METADATA.keys())}"
        )

    candidates = []
    for voice_id, meta in OPENAI_VOICE_METADATA.items():
        if locale and not meta["locale"].lower().startswith(locale.lower()):
            continue
        if gender and meta["gender"].lower() != gender.lower():
            continue
        candidates.append(
            VoiceInfo(
                voice_id=voice_id,
                name=meta["name"],
                locale=meta["locale"],
                gender=meta["gender"],
            )
        )

    if not candidates:
        candidates = list_vvoices()

    return candidates[0]


def get_voice_by_id(voice_id: str) -> VoiceInfo:
    if voice_id not in OPENAI_VOICE_METADATA:
        raise ValueError(
            f"OpenAI voice '{voice_id}' not found. Available: {list(OPENAI_VOICE_METADATA.keys())}"
        )
    meta = OPENAI_VOICE_METADATA[voice_id]
    return VoiceInfo(
        voice_id=voice_id,
        name=meta["name"],
        locale=meta["locale"],
        gender=meta["gender"],
    )
