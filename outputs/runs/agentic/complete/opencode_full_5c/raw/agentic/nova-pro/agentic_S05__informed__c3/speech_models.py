class TranscriptionRequest:
    def __init__(self, language_code, media_encoding, media_sample_rate_hertz):
        self.language_code = language_code
        self.media_encoding = media_encoding
        self.media_sample_rate_hertz = media_sample_rate_hertz


class TranscriptionResponse:
    def __init__(self, transcription_job_name):
        self.transcription_job_name = transcription_job_name
