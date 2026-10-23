import os
import boto3

def synthesize_text_aws_polly(text: str, voice_id: str = 'Joanna', output_format: str = 'mp3') -> bytes:
    client = boto3.client(
        'polly',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    if 'AudioStream' in response:
        return response['AudioStream'].read()
    return b''
