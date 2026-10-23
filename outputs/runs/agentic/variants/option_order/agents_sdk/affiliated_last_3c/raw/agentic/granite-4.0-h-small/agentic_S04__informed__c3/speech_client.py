import boto3

def get_transcribe_client():
    # Configure Amazon Transcribe client
    client = boto3.client(
        service_name='transcribe',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    return client