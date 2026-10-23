import boto3
from botocore.exceptions import NoCredentialsError

def get_speech_client():
    try:
        client = boto3.client('transcribestreaming')
        return client
    except NoCredentialsError:
        raise Exception('AWS credentials not found')

def create_stream_request(language_code='en-US'):
    return {
        'LanguageCode': language_code,
        'Media': {
            'MediaFileUri': 's3://your-bucket/your-audio-file'
        }
    }