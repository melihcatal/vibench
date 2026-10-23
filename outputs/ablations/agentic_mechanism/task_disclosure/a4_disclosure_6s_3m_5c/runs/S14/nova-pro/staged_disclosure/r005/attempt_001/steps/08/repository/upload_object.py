import boto3

def upload_to_s3(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f'File uploaded successfully to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

# Example usage
# upload_to_s3('my-bucket', 'my-object-key', 'path/to/my/file.txt')