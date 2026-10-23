import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

# Set up client
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')
speech_config = SpeechConfig(subscription=speech_key, region=speech_region)

# Poll a transcription job and return the transcript
def poll_transcription(job_id):
 recognizer = SpeechRecognizer(speech_config=speech_config)
 result = recognizer.get_transcription_result(job_id)
 if result.reason == ResultReason.RecognizedSpeech:
 return result.text
 else:
 return 'Polling failed'

if __name__ == '__main__':
 job_id = 'transcription_job_id'
 print(poll_transcription(job_id))