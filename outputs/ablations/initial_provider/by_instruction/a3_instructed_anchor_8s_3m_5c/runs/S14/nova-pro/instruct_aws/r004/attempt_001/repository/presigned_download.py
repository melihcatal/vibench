import boto3
from storage_client import get_s3_client

def create_presigned_url(bucket, key, expiration=3600):
    s3_client = get_s3_client()
    return s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expiration)