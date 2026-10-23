class TranscriptionRequest:
    def __init__(self, audio_file_uri, output_bucket_uri, job_name, language_code='en-US', media_format='mp3'):
        self.audio_file_uri = audio_file_uri
        self.output_bucket_uri = output_bucket_uri
        self.job_name = job_name
        self.language_code = language_code
        self.media_format = media_format

class TranscriptionResponse:
    def __init__(self, transcription_job):
        self.transcription_job = transcription_job

    def get_transcript_uri(self):
        return self.transcription_job['Transcript']['TranscriptFileUri'] if self.transcription_job['TranscriptionJobStatus'] == 'COMPLETED' else None