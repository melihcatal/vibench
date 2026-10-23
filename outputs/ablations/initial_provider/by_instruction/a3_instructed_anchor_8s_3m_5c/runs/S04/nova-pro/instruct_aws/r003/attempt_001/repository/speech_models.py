class TranscriptionRequest:
    def __init__(self, audio_file_uri, output_bucket_uri):
        self.audio_file_uri = audio_file_uri
        self.output_bucket_uri = output_bucket_uri

class TranscriptionResponse:
    def __init__(self, transcript_uri):
        self.transcript_uri = transcript_uri