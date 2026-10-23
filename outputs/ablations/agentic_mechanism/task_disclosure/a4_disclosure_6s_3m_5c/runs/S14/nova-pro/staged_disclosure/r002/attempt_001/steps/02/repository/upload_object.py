import boto3

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

def upload_to_s3(bucket_name, file_name):
    try:
        # Upload the file
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded {file_name} to {bucket_name}")
    except Exception as e:
        print(e)

# Example usage
# upload_to_s3('your-bucket-name', 'your-file-name')