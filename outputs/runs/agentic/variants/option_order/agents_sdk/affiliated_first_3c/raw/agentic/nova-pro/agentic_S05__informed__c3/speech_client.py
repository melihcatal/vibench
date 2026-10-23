import boto3
from botocore.exceptions import NoCredentialsError

transcribe = boto3.client('transcribe', region_name='us-west-2')

def get_transcribe_client():
    try:
        return transcribe
    except NoCredentialsError:
        print('No AWS credentials found')