class TranscriptionRequest:
    def __init__(self, audio_file_uri, output_bucket_uri):
        self.audio_file_uri = audio_file_uri
        self.output_bucket_uri = output_bucket_uri

class TranscriptionResponse:
    def __init__(self, job_name, transcript_uri):
        self.job_name = job_name
        self.transcript_uri = transcript_uri