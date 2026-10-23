import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

# Set up client
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

# Request speaker diarization for a recorded meeting
def diarized_transcript(audio_file_path):
 audio_config = AudioConfig(filename=audio_file_path)
 recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
 result = recognizer.recognize_once_async()
 if result.reason == ResultReason.RecognizedSpeech:
 return result.text
 else:
 return 'Diarization failed'

if __name__ == '__main__':
 audio_file_path = 'path_to_audio_file.wav'
 print(diarized_transcript(audio_file_path))