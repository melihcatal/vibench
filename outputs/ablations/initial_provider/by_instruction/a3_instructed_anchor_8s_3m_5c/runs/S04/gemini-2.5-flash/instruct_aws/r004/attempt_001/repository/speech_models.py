# speech_models.py
# This file can be used to define local request, response, and normalization helpers
# for Batch Speech-to-Text if needed.

# Example of a simple model placeholder (not strictly necessary for basic AWS SDK usage)
class TranscriptionJobRequest:
    def __init__(self, audio_uri: str, language_code: str):
        self.audio_uri = audio_uri
        self.language_code = language_code

class TranscriptionJobResponse:
    def __init__(self, job_name: str, job_status: str):
        self.job_name = job_name
        self.job_status = job_status
