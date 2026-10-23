import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config

def select_voice(config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    voices = synthesizer.get_voices_async().get()
    if voices.reason!= speechsdk.ResultReason.VoicesListReceived:
        raise RuntimeError('Failed to retrieve voices')
    return [voice.short_name for voice in voices.voices]