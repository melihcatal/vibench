import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuration
AWS_REGION = 'us-west-2'

# Client Helper Utilities
def create_transcribe_client():
    try:
        client = boto3.client('transcribe', region_name=AWS_REGION)
        return client
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception('AWS credentials not found or incomplete') from e

def start_transcription_job(client, job_name, media_file_uri, output_bucket_name):
    try:
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_file_uri},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName=output_bucket_name
        )
        return response
    except Exception as e:
        raise Exception('Failed to start transcription job') from e
