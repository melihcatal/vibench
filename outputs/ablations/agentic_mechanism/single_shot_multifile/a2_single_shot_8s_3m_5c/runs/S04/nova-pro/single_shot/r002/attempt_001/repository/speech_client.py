import os
import requests

class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CLOUD_SPEECH_API_KEY')
        self.base_url = 'https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def submit_transcription(self, file_path):
        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        data = {
            'config': {
                'encoding': 'LINEAR16',
                'sampleRateHertz': 16000,
                'languageCode': 'en-US'
            },
            'audio': {
                'content': str(audio_content)
            }
        }
        response = requests.post(self.base_url, json=data, headers=self.headers)
        return response.json()

    def poll_transcription(self, job_id):
        url = f'https://speech.googleapis.com/v1p1beta1/operations/{job_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def diarized_transcript(self, file_path):
        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        data = {
            'config': {
                'enableSpeakerDiarization': True,
                'diarizationSpeakerCount': 2,
                'encoding': 'LINEAR16',
               'sampleRateHertz': 16000,
                'languageCode': 'en-US'
            },
            'audio': {
                'content': str(audio_content)
            }
        }
        response = requests.post(self.base_url, json=data, headers=self.headers)
        return response.json()

    def timestamped_transcript(self, job_id):
        url = f'https://speech.googleapis.com/v1p1beta1/operations/{job_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()