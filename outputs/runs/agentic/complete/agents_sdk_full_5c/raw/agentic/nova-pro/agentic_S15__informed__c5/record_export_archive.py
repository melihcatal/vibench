import os
import boto3

s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-west-2')

def export_record(bucket_name, file_name, file_content):
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)