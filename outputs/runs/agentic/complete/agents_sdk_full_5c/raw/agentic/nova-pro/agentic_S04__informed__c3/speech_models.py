class TranscriptionJob:
    def __init__(self, job_name, status):
        self.job_name = job_name
        self.status = status

class Transcript:
    def __init__(self, transcript_uri):
        self.transcript_uri = transcript_uri