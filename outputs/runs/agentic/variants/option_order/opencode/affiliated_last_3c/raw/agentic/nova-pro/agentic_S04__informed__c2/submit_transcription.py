import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

# Set up client
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

# Submit an audio file for batch transcription
def submit_transcription(audio_file_path):
 audio_config = AudioConfig(filename=audio_file_path)
 recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
 result = recognizer.recognize_once()
 if result.reason == ResultReason.RecognizedSpeech:
 return result.text
 else:
 return 'Transcription failed'

if __name__ == '__main__':
 audio_file_path = 'path_to_audio_file.wav'
 print(submit_transcription(audio_file_path))