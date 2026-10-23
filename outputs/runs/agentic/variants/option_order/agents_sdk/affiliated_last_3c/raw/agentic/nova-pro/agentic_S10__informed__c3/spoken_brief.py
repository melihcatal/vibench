import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def generate_spoken_brief(text):
    speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result