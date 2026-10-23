class TranscriptionRequest:
    def __init__(self, file_uri, job_name, language_code='en-US'):
        self.file_uri = file_uri
        self.job_name = job_name
        self.language_code = language_code

class TranscriptionResponse:
    def __init__(self, job):
        self.job = job

    def get_transcript(self):
        return self.job['Transcript']['TranscriptFileUri'] if self.job['TranscriptionJobStatus'] == 'COMPLETED' else None