import azure.cognitiveservices.speech as speechsdk

from speech_client import ensure_azure_config
from speech_models import VoiceInfo


def select_voice(locale: str) -> list[VoiceInfo]:
    config = ensure_azure_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    voices = synthesizer.get_voices_async(locale).get().voices
    return [
        VoiceInfo(name=v.short_name, locale=v.locale, gender=str(v.gender))
        for v in voices
    ]
