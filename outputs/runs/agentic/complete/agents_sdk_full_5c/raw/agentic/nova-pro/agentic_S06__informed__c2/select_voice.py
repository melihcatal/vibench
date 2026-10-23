import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

def select_voice(locale):
    voices = speech_synthesizer.get_voices()
    for voice in voices.voices:
        if voice.locale == locale:
            return voice.name
    return None