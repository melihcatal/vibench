import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, SpeechSynthesisOutputFormat

# Set up the Azure Speech service configuration
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

def submit_transcription(audio_file_path):
    config = SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = AudioConfig(filename=audio_file_path)
    recognizer = SpeechRecognizer(speech_config=config, audio_config=audio_config)
    result = recognizer.recognize_once()
    if result.reason == ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None