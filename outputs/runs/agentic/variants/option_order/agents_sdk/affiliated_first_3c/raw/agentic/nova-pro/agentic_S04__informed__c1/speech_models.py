class TranscriptionRequest:
    def __init__(self, audio_uri, job_name, media_format='mp3', language_code='en-US'):
        self.audio_uri = audio_uri
        self.job_name = job_name
        self.media_format = media_format
        self.language_code = language_code

class TranscriptionResponse:
    def __init__(self, job):
        self.job = job

    def is_completed(self):
        return self.job['TranscriptionJobStatus'] == 'COMPLETED'

    def get_transcript(self):
        return self.job['Transcript'] if self.is_completed() else None