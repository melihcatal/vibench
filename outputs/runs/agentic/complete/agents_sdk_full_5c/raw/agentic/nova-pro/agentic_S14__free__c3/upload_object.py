import boto3

def upload_object(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    with open(file_path, 'rb') as data:
        s3_client.upload_fileobj(data, bucket_name, object_key))