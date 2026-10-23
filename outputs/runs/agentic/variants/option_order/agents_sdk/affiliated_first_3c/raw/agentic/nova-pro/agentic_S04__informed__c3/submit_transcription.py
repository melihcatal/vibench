import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognitionMode, SpeechSynthesizer, SpeechRecognizer

speech_config = SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))

def submit_transcription(audio_file):
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_filename=audio_file)
    result = recognizer.recognize_once()
    return result.text