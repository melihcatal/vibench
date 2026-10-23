import os

def get_aws_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')

def get_s3_archive_bucket() -> str:
    bucket = os.getenv('S3_ARCHIVE_BUCKET')
    if not bucket:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable is required.")
    return bucket
