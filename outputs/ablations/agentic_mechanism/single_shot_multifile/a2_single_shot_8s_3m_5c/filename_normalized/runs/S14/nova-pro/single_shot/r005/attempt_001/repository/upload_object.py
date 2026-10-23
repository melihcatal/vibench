import boto3
from storage_client import get_s3_client

def upload_object(bucket_name, object_key, file_path):
    s3_client = get_s3_client()
    with open(file_path, 'rb') as file_data:
        s3_client.upload_fileobj(file_data, bucket_name, object_key)

if __name__ == '__main__':
    upload_object('my-bucket','my-object', 'local-file.txt')