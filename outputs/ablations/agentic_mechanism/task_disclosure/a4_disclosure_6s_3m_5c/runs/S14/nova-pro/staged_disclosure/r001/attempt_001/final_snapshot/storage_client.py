import boto3

def create_s3_client():
    return boto3.client('s3')

def upload_to_s3(bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = create_s3_client()
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(f'File {file_name} uploaded to {bucket_name}/{object_name}')
    except Exception as e:
        print(e)
        return False
    return True

def download_from_s3(bucket_name, object_name, file_name):
    s3_client = create_s3_client()
    try:
        response = s3_client.download_file(bucket_name, object_name, file_name)
        print(f'File {object_name} downloaded from {bucket_name} to {file_name}')
    except Exception as e:
        print(e)
        return False
    return True