import boto3

# Initialize a session using Amazon S3
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

s3 = session.client('s3')

# Function to upload files to S3
def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path
    try:
        response = s3.upload_file(file_path, bucket_name, object_name)
        print(f'File {file_path} uploaded to {bucket_name}/{object_name}')
    except Exception as e:
        print(e)

# Example usage
upload_to_s3('path/to/your/file', 'your-bucket-name')