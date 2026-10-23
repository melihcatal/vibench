import os
import boto3

def archive_metrics(bucket_name, object_key, file_path):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    s3.upload_file(file_path, bucket_name, object_key)