class TranscriptionRequest:
    def __init__(self, audio_file_uri, output_bucket_uri, media_format='mp3', language_code='en-US'):
        self.audio_file_uri = audio_file_uri
        self.output_bucket_uri = output_bucket_uri
        self.media_format = media_format
        self.language_code = language_code

class TranscriptionResponse:
    def __init__(self, job_name, transcript_uri):
        self.job_name = job_name
        self.transcript_uri = transcript_uri