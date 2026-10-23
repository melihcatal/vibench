import os
import requests

class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CLOUD_SPEECH_API_KEY')
        self.base_url = 'https://speech.googleapis.com/v1p1beta1/'

    def submit_transcription_job(self, audio_file_path):
        url = self.base_url + 'speech:asyncrecognize'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'config': {
                'encoding': 'LINEAR16',
               'sampleRateHertz': 16000,
                'languageCode': 'en-US'
            },
            'audio': {'uri': f'gs://{audio_file_path}'}
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def poll_transcription_job(self, job_id):
        url = self.base_url + f'operations/{job_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def submit_diarization_job(self, audio_file_path):
        url = self.base_url +'speech:diarize'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'config': {
                'enableSpeakerDiarization': True,
                'diarizationSpeakerCount': 2
            },
            'audio': {'uri': f'gs://{audio_file_path}'}
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def poll_diarization_job(self, job_id):
        url = self.base_url + f'operations/{job_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_timestamped_transcript(self, job_id):
        url = self.base_url + f'operations/{job_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()