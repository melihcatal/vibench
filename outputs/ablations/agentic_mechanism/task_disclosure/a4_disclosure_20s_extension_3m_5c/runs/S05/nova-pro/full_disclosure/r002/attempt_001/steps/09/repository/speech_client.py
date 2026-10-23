import boto3

class SpeechClient:
    def __init__(self, region_name='us-west-2'):
        self.transcribe_client = boto3.client('transcribe', region_name=region_name)

    def start_stream_transcription(self, language_code, media_sample_rate_hz, media_encoding):
        response = self.transcribe_client.start_stream_transcription(
            LanguageCode=language_code,
            MediaSampleRateHertz=media_sample_rate_hz,
            MediaEncoding=media_encoding
        )
        return response

    def get_transcription_results(self, session_id):
        response = self.transcribe_client.get_transcription_results(
            TranscriptionJobName=session_id
        )
        return response
