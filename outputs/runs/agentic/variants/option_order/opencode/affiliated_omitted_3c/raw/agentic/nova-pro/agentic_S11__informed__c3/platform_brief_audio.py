import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


def generate_audio(text):
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data
