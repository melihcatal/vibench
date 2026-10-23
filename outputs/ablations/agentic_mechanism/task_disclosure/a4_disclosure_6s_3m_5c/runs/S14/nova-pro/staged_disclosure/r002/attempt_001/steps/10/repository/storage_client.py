import boto3

# Configuration for AWS S3
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
region_name = 'us-west-2'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
    if object_name is None:
        object_name = file_name
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f'File {file_name} uploaded to {bucket}/{object_name}')
    except Exception as e:
        print(e)
        return False
    return True