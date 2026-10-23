from azure.cognitiveservices.speech import SpeechSynthesizer

from speech_client import create_speech_config


def select_voice(locale: str = None):
    speech_config = create_speech_config()
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    voices = synthesizer.get_voices_async(locale).get().voices
    return [voice.name for voice in voices]
