class TranscriptionRequest:
    def __init__(self, file_uri, job_name, language_code="en-US"):
        self.file_uri = file_uri
        self.job_name = job_name
        self.language_code = language_code


class TranscriptionResponse:
    def __init__(self, job_name, transcription_result):
        self.job_name = job_name
        self.transcription_result = transcription_result
