import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

# Set up the Azure Speech TTS client
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)


def save_audio(audio_data, file_path):
    with open(file_path, "wb") as f:
        f.write(audio_data)
