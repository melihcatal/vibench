import httpx
from typing import List, Optional
from speech_client import (
    OPENAI_CHAT_ENDPOINT,
    get_openai_headers,
    create_http_client,
    build_chat_payload,
    validate_openai_key,
    OPENAI_VOICES,
    DEFAULT_CHAT_MODEL,
)
from speech_models import VoiceInfo, normalize_voice_id


OPENAI_VOICE_METADATA = {
    "alloy": {
        "name": "Alloy",
        "locale": "en-US",
        "gender": "neutral",
        "styles": ["neutral", "narration", "conversational"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
    "echo": {
        "name": "Echo",
        "locale": "en-US",
        "gender": "male",
        "styles": ["neutral", "narration"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
    "fable": {
        "name": "Fable",
        "locale": "en-GB",
        "gender": "male",
        "styles": ["neutral", "narration", "expressive"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
    "onyx": {
        "name": "Onyx",
        "locale": "en-US",
        "gender": "male",
        "styles": ["neutral", "narration", "authoritative"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
    "nova": {
        "name": "Nova",
        "locale": "en-US",
        "gender": "female",
        "styles": ["neutral", "narration", "warm"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
    "shimmer": {
        "name": "Shimmer",
        "locale": "en-US",
        "gender": "female",
        "styles": ["neutral", "narration", "light"],
        "sample_rate_hz": 24000,
        "is_neural": True,
    },
}


def list_voices() -> List[VoiceInfo]:
    voices = []
    for voice_id, meta in OPENAI_VOICE_METADATA.items():
        voices.append(
            VoiceInfo(
                voice_id=voice_id,
                name=meta["name"],
                locale=meta["locale"],
                gender=meta["gender"],
                styles=meta["styles"],
                sample_rate_hz=meta["sample_rate_hz"],
                is_neural=meta["is_neural"],
            )
        )
    return voices


def select_voice(
    locale: Optional[str] = None,
    gender: Optional[str] = None,
    style: Optional[str] = None,
) -> VoiceInfo:
    candidates = list_voices()

    if locale:
        locale_lower = locale.lower()
        candidates = [v for v in candidates if locale_lower in v.locale.lower()]

    if gender:
        gender_lower = gender.lower()
        candidates = [v for v in candidates if v.gender.lower() == gender_lower]

    if style:
        style_lower = style.lower()
        candidates = [
            v for v in candidates if style_lower in [s.lower() for s in v.styles]
        ]

    if not candidates:
        candidates = list_voices()

    return candidates[0]


def recommend_voice(
    text: str,
    target_locale: str = "en-US",
) -> VoiceInfo:
    if not validate_openai_key():
        return select_voice(locale=target_locale)

    system_msg = {
        "role": "system",
        "content": (
            "You are a voice selection assistant. Given a text snippet and target locale, "
            "recommend the best OpenAI TTS voice from: alloy, echo, fable, onyx, nova, shimmer. "
            "Respond with ONLY the voice name in lowercase."
        ),
    }
    user_msg = {
        "role": "user",
        "content": f"Text: {text}\nTarget locale: {target_locale}\nRecommend a voice:",
    }

    payload = build_chat_payload(
        messages=[system_msg, user_msg],
        model=DEFAULT_CHAT_MODEL,
    )

    with create_http_client() as client:
        response = client.post(
            OPENAI_CHAT_ENDPOINT,
            headers=get_openai_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    recommended = data["choices"][0]["message"]["content"].strip().lower()
    normalized = normalize_voice_id(recommended)

    return (
        select_voice(locale=target_locale)
        if normalized not in OPENAI_VOICES
        else VoiceInfo(
            voice_id=normalized,
            name=OPENAI_VOICE_METADATA[normalized]["name"],
            locale=OPENAI_VOICE_METADATA[normalized]["locale"],
            gender=OPENAI_VOICE_METADATA[normalized]["gender"],
            styles=OPENAI_VOICE_METADATA[normalized]["styles"],
            sample_rate_hz=OPENAI_VOICE_METADATA[normalized]["sample_rate_hz"],
            is_neural=OPENAI_VOICE_METADATA[normalized]["is_neural"],
        )
    )
