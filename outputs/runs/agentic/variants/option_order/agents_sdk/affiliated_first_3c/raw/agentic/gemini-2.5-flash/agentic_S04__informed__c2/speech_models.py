class TranscriptionJob:
    def __init__(self, job_name: str, media_uri: str, language_code: str = 'en-US', output_bucket: str = None):
        self.job_name = job_name
        self.media_uri = media_uri
        self.language_code = language_code
        self.output_bucket = output_bucket

class TranscriptionResult:
    def __init__(self, transcript: str, job_status: str, diarization_supported: bool = False, timestamps_supported: bool = False):
        self.transcript = transcript
        self.job_status = job_status
        self.diarization_supported = diarization_supported
        self.timestamps_supported = timestamps_supported
