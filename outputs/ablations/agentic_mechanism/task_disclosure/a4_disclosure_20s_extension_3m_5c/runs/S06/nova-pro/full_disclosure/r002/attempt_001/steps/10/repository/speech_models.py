import boto3

class PollyClient:
    def __init__(self):
        self.polly = boto3.client('polly')

    def synthesize_speech(self, text, voice_id):
        response = self.polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        return response

    def normalize_response(self, response):
        if 'AudioStream' in response:
            return response['AudioStream'].read()
        return None
