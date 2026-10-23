class TranscriptionJob:
    def __init__(self, job_name, status, transcript_uri):
        self.job_name = job_name
        self.status = status
        self.transcript_uri = transcript_uri