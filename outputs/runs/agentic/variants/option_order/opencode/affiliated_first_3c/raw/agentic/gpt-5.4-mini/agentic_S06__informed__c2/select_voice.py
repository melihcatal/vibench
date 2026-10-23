import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config
from speech_models import normalize_locale


def select_voice(locale: str):
    config = get_speech_config()
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    voices = synthesizer.get_voices_async(normalize_locale(locale)).get().voices
    return [v.short_name for v in voices]
