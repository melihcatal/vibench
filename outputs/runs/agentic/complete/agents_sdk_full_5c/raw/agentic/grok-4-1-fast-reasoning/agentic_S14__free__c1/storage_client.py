import os

BUCKET_NAME = os.getenv('STORAGE_BUCKET')
if not BUCKET_NAME:
    raise ValueError('STORAGE_BUCKET environment variable is required.')

S3_CONFIG = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'region_name': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
}
