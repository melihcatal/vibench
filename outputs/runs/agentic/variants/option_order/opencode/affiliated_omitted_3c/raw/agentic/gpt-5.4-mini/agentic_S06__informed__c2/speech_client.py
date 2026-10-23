import os
from dataclasses import asdict
from typing import Iterable, List, Optional

import boto3

from speech_models import SpeechRequest, VoiceOption, normalize_locale, normalize_text


def load_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def make_polly_client():
    return boto3.client("polly", region_name=load_region())


def build_speech_request(
    text: str,
    voice: Optional[str] = None,
    locale: Optional[str] = None,
    format: str = "mp3",
) -> SpeechRequest:
    return SpeechRequest(
        text=normalize_text(text),
        voice=voice,
        locale=normalize_locale(locale),
        format=format,
    )


def voice_options_from_polly(voices: Iterable[dict]) -> List[VoiceOption]:
    options: List[VoiceOption] = []
    for voice in voices:
        options.append(
            VoiceOption(
                name=voice.get("Name", ""),
                locale=normalize_locale(voice.get("LanguageCode", "")) or "",
                gender=voice.get("Gender"),
                provider_id=voice.get("Id"),
            )
        )
    return options
