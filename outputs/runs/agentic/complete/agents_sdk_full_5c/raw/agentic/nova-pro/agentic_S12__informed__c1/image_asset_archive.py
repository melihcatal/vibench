import os
import boto3

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def archive_image_asset(bucket_name, file_path, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, object_name)