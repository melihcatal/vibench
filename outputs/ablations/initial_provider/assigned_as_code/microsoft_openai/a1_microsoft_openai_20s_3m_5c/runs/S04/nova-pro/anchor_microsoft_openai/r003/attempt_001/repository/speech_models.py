class TranscriptionRequest:
    def __init__(self, audio_uri, output_bucket):
        self.audio_uri = audio_uri
        self.output_bucket = output_bucket

class TranscriptionResponse:
    def __init__(self, job_name, status):
        self.job_name = job_name
        self.status = status

def normalize_transcription_response(response):
    return TranscriptionResponse(response['TranscriptionJob']['TranscriptionJobName'], response['TranscriptionJob']['TranscriptionJobStatus'])