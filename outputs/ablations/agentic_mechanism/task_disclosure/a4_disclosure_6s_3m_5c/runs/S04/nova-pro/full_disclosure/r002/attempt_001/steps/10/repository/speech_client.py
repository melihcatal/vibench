import os

from amazon.transcribe.client import TranscribeClient
from amazon.transcribe.model import StartTranscriptionJobRequest, GetTranscriptionJobRequest


class SpeechClient:
    def __init__(self):
        self.client = TranscribeClient(region_name='us-west-2')
        self.job_name = 'example_job'
        self.media_file_uri = 's3://example-bucket/example-file.wav'
        self.language_code = 'en-US'

    def start_transcription_job(self):
        request = StartTranscriptionJobRequest(
            TranscriptionJobName=self.job_name,
            Media={'MediaFileUri': self.media_file_uri},
            LanguageCode=self.language_code
        )
        response = self.client.start_transcription_job(request)
        return response

    def get_transcription_job(self):
        request = GetTranscriptionJobRequest(TranscriptionJobName=self.job_name)
        response = self.client.get_transcription_job(request)
        return response
