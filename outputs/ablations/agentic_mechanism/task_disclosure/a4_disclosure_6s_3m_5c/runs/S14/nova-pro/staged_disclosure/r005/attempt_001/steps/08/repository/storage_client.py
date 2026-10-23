import boto3

def configure_s3_client():
    return boto3.client('s3')

def upload_to_s3(bucket_name, file_path, object_name=None):
    if object_name is None:
        object_name = file_path
    s3_client = configure_s3_client()
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f'File uploaded successfully to {bucket_name}/{object_name}')
    except Exception as e:
        print(e)

def download_from_s3(bucket_name, object_name, file_path):
    s3_client = configure_s3_client()
    try:
        response = s3_client.download_file(bucket_name, object_name, file_path)
        print(f'File downloaded successfully from {bucket_name}/{object_name}')
    except Exception as e:
        print(e)