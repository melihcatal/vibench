import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from typing import List, Optional


def list_voices(locale: Optional[str] = None) -> List[dict]:
    speech_config = get_speech_config()
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    result = speech_synthesizer.get_voices_async(locale).get()
    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        return [
            {
                "name": voice.name,
                "locale": voice.locale,
                "gender": voice.gender.name,
                "short_name": voice.short_name,
            }
            for voice in result.voices
        ]
    else:
        raise Exception(f"Failed to list voices: {result.reason}")


def select_voice(locale: str, gender: Optional[str] = None) -> dict:
    voices = list_voices(locale)
    for voice in voices:
        if gender and voice["gender"] != gender:
            continue
        return voice
    raise ValueError(f"No voice found for locale {locale} and gender {gender}")