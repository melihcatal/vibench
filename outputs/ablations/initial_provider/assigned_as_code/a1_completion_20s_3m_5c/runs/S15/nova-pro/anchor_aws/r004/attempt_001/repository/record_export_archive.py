import boto3

s3 = boto3.client('s3', region_name='us-west-2')

def export_record_to_s3(bucket_name, key, record):
    s3.put_object(Bucket=bucket_name, Key=key, Body=str(record))