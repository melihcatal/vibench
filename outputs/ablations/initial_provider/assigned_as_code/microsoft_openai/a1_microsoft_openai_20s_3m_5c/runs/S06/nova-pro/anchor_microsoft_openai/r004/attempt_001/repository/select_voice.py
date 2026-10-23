import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def select_voice(config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    voices = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).get_voices()
    return [voice.short_name for voice in voices if voice.locale == config.get('locale', 'en-US')]
