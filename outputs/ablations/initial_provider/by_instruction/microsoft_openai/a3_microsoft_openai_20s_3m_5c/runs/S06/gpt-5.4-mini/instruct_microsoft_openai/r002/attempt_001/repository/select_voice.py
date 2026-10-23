from typing import List

from speech_client import select_matching_voice
from speech_models import VoiceChoice


def list_voices() -> List[VoiceChoice]:
    return [
        VoiceChoice(name="alloy", locale="en-US", gender="neutral", short_name="alloy"),
        VoiceChoice(name="echo", locale="en-GB", gender="neutral", short_name="echo"),
        VoiceChoice(name="fable", locale="en-AU", gender="neutral", short_name="fable"),
    ]


def select_voice(target_locale: str | None = None) -> VoiceChoice | None:
    return select_matching_voice(list_voices(), target_locale)
