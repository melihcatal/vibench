import os
import boto3

def object_metadata(bucket_name, object_key):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    metadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    return metadata