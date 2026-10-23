import boto3
from botocore.exceptions import NoCredentialsError

transcribe = boto3.client('transcribe', region_name='us-west-2')

def handle_partial_results(transcription_stream):
    try:
        for event in transcription_stream:
            if 'TranscriptEvent' in event:
                print(event['TranscriptEvent'])
    except NoCredentialsError:
        print('No AWS credentials found')