class TranscriptionRequest:
    def __init__(self, audio_file_uri, job_name, media_format='mp4', language_code='en-US'):
        self.audio_file_uri = audio_file_uri
        self.job_name = job_name
        self.media_format = media_format
        self.language_code = language_code

class TranscriptionResponse:
    def __init__(self, job):
        self.job = job