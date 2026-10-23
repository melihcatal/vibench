import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_spoken_briefing(text):
    speech_key = os.getenv('SPEECH_KEY')
    service_region = os.getenv('SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data