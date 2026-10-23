import boto3

def archive_record(bucket_name, key, file_content):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=key, Body=file_content)