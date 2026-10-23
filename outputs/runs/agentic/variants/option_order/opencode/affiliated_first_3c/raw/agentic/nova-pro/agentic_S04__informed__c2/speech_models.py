class TranscriptionRequest:
    def __init__(self, audio_file_uri):
        self.audio_file_uri = audio_file_uri


class TranscriptionResponse:
    def __init__(self, job_name, status):
        self.job_name = job_name
        self.status = status
