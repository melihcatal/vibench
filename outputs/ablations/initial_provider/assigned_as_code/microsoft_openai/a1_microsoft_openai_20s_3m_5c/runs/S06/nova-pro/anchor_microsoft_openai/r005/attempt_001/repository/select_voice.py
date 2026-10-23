import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config

def select_voice(locale):
    speech_config = get_speech_config({})
    voices = speechsdk.SpeechSynthesisVoice(speech_config)
    return [voice.short_name for voice in voices if voice.locale == locale]