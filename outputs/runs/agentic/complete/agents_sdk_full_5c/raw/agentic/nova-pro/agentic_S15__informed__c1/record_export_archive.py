import os
from boto3 import client
s3 = client('s3')

def export_archive(bucket_name, object_name, file_path):
    s3.upload_file(file_path, bucket_name, object_name)