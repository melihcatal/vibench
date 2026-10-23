import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config

def select_voice(config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    voices = speechsdk.SpeechSynthesisVoice.from_config(speech_config)
    return [{'name': voice.name, 'locale': voice.language} for voice in voices]