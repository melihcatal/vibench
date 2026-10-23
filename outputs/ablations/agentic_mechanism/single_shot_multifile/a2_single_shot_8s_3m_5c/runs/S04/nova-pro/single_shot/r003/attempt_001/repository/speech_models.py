class TranscriptionJob:
    def __init__(self, job_id):
        self.job_id = job_id

class TranscriptionResult:
    def __init__(self, transcript):
        self.transcript = transcript

class DiarizationJob:
    def __init__(self, job_id):
        self.job_id = job_id

class DiarizationResult:
    def __init__(self, diarized_transcript):
        self.diarized_transcript = diarized_transcript

class TimestampedTranscript:
    def __init__(self, timestamped_transcript):
        self.timestamped_transcript = timestamped_transcript