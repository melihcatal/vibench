import os
import requests

class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
        self.base_url = 'https://speech.googleapis.com/v1p1beta1/'

    def submit_transcription(self, file_path):
        with open(file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            params = {'key': self.api_key}
            response = requests.post(self.base_url + 'operations:asyncrecognize', files=files, params=params)
            response.raise_for_status()
            return response.json()

    def poll_transcription(self, job_id):
        params = {'key': self.api_key}
        response = requests.get(self.base_url + 'operations/' + job_id, params=params)
        response.raise_for_status()
        return response.json()

    def diarized_transcript(self, job_id):
        params = {'key': self.api_key, 'diarizationSpeakerCount': 2}
        response = requests.get(self.base_url + 'operations/' + job_id, params=params)
        response.raise_for_status()
        return response.json()

    def timestamped_transcript(self, job_id):
        params = {'key': self.api_key, 'enableWordTimeOffsets': True}
        response = requests.get(self.base_url + 'operations/' + job_id, params=params)
        response.raise_for_status()
        return response.json()