import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_audio(text):
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    service_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()
    return result.audio_data