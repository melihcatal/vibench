import boto3

class SpeechToTextModel:
    def __init__(self):
        self.transcribe_client = boto3.client('transcribe')

    def create_transcription_job(self, job_name, language_code, media_file_uri):
        response = self.transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            Media={'MediaFileUri': media_file_uri},
            Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
        )
        return response

    def get_transcription_job(self, job_name):
        response = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        return response

    def normalize_transcription(self, transcription):
        # Placeholder for normalization logic
        return transcription
