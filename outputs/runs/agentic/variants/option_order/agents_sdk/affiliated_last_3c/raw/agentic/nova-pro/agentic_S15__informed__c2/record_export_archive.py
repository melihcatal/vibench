import boto3

s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')

def upload_to_s3(bucket_name, file_name, file_content):
    s3.upload_fileobj(file_content, bucket_name, file_name)