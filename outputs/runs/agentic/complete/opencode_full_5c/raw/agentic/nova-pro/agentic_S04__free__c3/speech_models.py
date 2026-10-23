class TranscriptionRequest:
    def __init__(
        self, audio_file_path, job_name, media_format="mp3", language_code="en-US"
    ):
        self.audio_file_path = audio_file_path
        self.job_name = job_name
        self.media_format = media_format
        self.language_code = language_code


class TranscriptionResponse:
    def __init__(self, status, transcript_uri):
        self.status = status
        self.transcript_uri = transcript_uri
