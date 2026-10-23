class TranscriptionJob:
    def __init__(self, job_id, status, results):
        self.job_id = job_id
        self.status = status
        self.results = results


class TranscriptionResult:
    def __init__(self, transcript, timestamps):
        self.transcript = transcript
        self.timestamps = timestamps
