import boto3

def upload_to_s3(bucket_name, file_path, object_name=None):
    s3_client = boto3.client('s3')
    if not object_name:
        object_name = file_path
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f'File {file_path} uploaded to {bucket_name}/{object_name}')
    except Exception as e:
        print(e)
        raise

# Example usage:
# upload_to_s3('my-bucket', 'path/to/local/file.txt')