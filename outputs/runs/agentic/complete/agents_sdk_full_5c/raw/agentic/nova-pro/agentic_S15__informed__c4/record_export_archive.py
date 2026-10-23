import boto3

def export_to_s3(bucket_name, file_name, file_content):
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)