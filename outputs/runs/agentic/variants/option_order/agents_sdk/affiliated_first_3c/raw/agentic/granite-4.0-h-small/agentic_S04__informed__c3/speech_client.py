# [HELPER] speech_client.py
import os
import json
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class SpeechClient:
    def __init__(self):
        apikey = os.getenv('IBM_STT_APIKEY')
        url = os.getenv('IBM_STT_URL')
        if not apikey or not url:
            raise RuntimeError('Set IBM_STT_APIKEY and IBM_STT_URL environment variables')
        self.authenticator = IAMAuthenticator(apikey)
        self.service = SpeechToTextV1(authenticator=self.authenticator)
        self.service.set_service_url(url)

    def submit_batch_transcription(self, payload):
        # Submit a batch job request
        response = self.service.create_job(payload).get_result()
        return response.get('created_job_id')

    def get_job_status(self, job_id):
        response = self.service.get_job(job_id).get_result()
        return response

    def get_transcript(self, job_id):
        result = self.get_job_status(job_id)
        if result['status'] == 'completed':
            return result.get('results', [{}])[0].get('alternatives', [{}])[0].get('transcript')
        raise RuntimeError(f'Job {job_id} not completed')

    def get_timestamps(self, job_id):
        result = self.get_job_status(job_id)
        if result['status'] == 'completed':
            return result.get('results', [{}])[0].get('alternatives', [{}])[0].get('timestamps')
        raise RuntimeError(f'Job {job_id} not completed')

    def diarize(self, payload):
        # Submit batch job with diarization enabled
        return self.submit_batch_transcription(payload)
