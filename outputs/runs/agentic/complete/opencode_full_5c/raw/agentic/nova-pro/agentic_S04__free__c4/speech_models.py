class TranscriptionRequest:
    def __init__(self, audio_file_uri, job_name):
        self.audio_file_uri = audio_file_uri
        self.job_name = job_name


class TranscriptionResponse:
    def __init__(self, job_name, transcript):
        self.job_name = job_name
        self.transcript = transcript
