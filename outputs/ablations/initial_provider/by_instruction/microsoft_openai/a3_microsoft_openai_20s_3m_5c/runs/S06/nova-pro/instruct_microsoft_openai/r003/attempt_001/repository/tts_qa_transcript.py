import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

def transcribe_audio(audio_path: str) -> str:
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    recognizer = SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once_async().get()
    return result.text