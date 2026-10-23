import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

def timestamped_transcript(audio_file_path):
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = AudioConfig(filename=audio_file_path)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text, result.duration
    else:
        return None, None