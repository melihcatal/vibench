import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

# Set up the Azure Speech TTS client
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)


def synthesize_text(text):
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data
