import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig


def diarized_transcript(audio_file_path):
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = AudioConfig(filename=audio_file_path)
    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once_async().get()
    return result.text
