import azure.cognitiveservices.speech as speechsdk

from speech_client import require_config
from speech_models import VoiceOption


def select_voice(locale: str | None = None) -> list[VoiceOption]:
    config = require_config()
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    voices = synthesizer.get_voices_async(locale or config.language).get().voices
    return [VoiceOption(name=v.name, locale=v.locale, gender=getattr(v, "gender", None), short_name=getattr(v, "short_name", None)) for v in voices]
