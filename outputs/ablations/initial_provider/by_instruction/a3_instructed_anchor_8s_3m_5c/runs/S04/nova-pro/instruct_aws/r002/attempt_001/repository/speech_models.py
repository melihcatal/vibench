class TranscriptionRequest:
    def __init__(self, file_uri, job_name, language_code):
        self.file_uri = file_uri
        self.job_name = job_name
        self.language_code = language_code

class TranscriptionResponse:
    def __init__(self, transcript_uri):
        self.transcript_uri = transcript_uri