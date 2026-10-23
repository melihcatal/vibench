class TranscriptionRequest:
    def __init__(self, audio_file_uri, output_bucket):
        self.audio_file_uri = audio_file_uri
        self.output_bucket = output_bucket


class TranscriptionResponse:
    def __init__(self, job_name, transcript):
        self.job_name = job_name
        self.transcript = transcript
