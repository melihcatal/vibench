import boto3

def export_to_s3(bucket_name, object_key, file_content):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)