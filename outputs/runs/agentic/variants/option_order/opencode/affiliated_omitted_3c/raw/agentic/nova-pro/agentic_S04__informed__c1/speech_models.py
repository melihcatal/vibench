class TranscriptionRequest:
    def __init__(self, audio_file_path, diarization=False, timestamps=False):
        self.audio_file_path = audio_file_path
        self.diarization = diarization
        self.timestamps = timestamps


class TranscriptionResponse:
    def __init__(self, job_id):
        self.job_id = job_id
