import os
import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_client():
    """Creates and returns a boto3 S3 client using environment credentials.
    Intended for Amazon S3 integrations in this project.
    """
    try:
        s3 = boto3.client('s3')
        # Test connectivity (optional)
        s3.head_bucket(Bucket=os.getenv('S3_TEST_BUCKET', 'your-test-bucket'))
        return s3
    except NoCredentialsError:
        raise RuntimeError('AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
