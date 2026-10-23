import boto3

def upload_to_s3(bucket_name, file_path, object_name=None):
    if object_name is None:
        object_name = file_path
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to {bucket_name}/{object_name}")
    except Exception as e:
        print(e)
        raise

# Example usage:
# upload_to_s3('your-bucket-name', 'path/to/your/file.jpg')