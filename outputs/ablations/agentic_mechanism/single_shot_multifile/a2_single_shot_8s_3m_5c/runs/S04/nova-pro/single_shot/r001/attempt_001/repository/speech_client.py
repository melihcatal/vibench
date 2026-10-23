import os
import requests

class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CLOUD_SPEECH_API_KEY')
        self.base_url = 'https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize'

    def submit_transcription(self, audio_file):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        files = {'audio': audio_file}
        response = requests.post(self.base_url, headers=headers, files=files)
        return response.json()

    def get_transcription_status(self, job_id):
        url = f'{self.base_url}/{job_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_transcription_result(self, job_id):
        url = f'{self.base_url}/{job_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def request_speaker_diarization(self, job_id):
        url = f'{self.base_url}/{job_id}:diarize'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(url, headers=headers)
        return response.json()