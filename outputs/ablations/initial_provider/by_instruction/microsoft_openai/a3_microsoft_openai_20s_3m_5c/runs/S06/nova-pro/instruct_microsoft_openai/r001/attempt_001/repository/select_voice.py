import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def select_voice(locale: str):
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices()
    for voice in voices['Voices']:
        if voice['Locale'] == locale:
            return voice['ShortName']
    return None