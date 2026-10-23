import os
import boto3

def list_prefix(bucket_name, prefix):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return objects.get('Contents', [])