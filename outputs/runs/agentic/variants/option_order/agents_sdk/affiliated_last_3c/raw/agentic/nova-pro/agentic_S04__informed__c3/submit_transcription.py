import os
from azure.cognitiveservices.speech.audio import AudioDataStream
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

def submit_transcription(audio_file_path):
    audio_input = AudioDataStream.from_wav_file(audio_file_path)
    recognizer = SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once_async(audio_input).get()
    return result.text