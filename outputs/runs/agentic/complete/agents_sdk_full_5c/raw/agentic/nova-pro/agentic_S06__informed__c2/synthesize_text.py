import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

def synthesize_text(text):
    result = speech_synthesizer.speak_text_async(text).get()
    return result.audio_data