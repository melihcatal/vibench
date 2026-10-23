import boto3

# Initialize a session using Amazon S3
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

s3 = session.resource('s3')

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        response = s3.Bucket(bucket).upload_file(file_name, object_name)
        print(f"Uploaded {file_name} to {bucket}/{object_name}")
    except Exception as e:
        print(e)
        raise

# Example usage
# upload_file('path/to/your/file', 'your-bucket-name')