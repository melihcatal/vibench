import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

# Set up the Azure Speech TTS client
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)


def select_voice(locale):
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices()
    for voice in voices.voices:
        if voice.locale == locale:
            return voice.short_name
    return None
