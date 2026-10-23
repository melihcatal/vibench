import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

def synthesize_ssml(ssml):
    result = speech_synthesizer.speak_ssml_async(ssml).get()
    return result.audio_data