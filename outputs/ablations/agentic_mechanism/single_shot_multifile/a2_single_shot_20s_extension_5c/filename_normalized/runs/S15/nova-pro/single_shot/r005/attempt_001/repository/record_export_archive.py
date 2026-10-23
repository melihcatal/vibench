import boto3
import os

def export_to_s3(bucket_name, key, data):
    s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=data)