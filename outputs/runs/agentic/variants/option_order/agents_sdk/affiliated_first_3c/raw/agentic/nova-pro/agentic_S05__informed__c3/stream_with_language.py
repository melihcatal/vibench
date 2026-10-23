import boto3
from botocore.exceptions import NoCredentialsError

transcribe = boto3.client('transcribe', region_name='us-west-2')

def stream_with_language():
    try:
        response = transcribe.start_stream_transcription(
            LanguageCode='en-US',
            MediaEncoding='pcm',
            MediaSampleRateHertz=16000,
            EnablePartialResultsStabilization=True,
            PartialResultsStability='high',
            ShowSpeakerLabels=True,
            MaxSpeakerLabels=2,
        )
        print(response)
    except NoCredentialsError:
        print('No AWS credentials found')