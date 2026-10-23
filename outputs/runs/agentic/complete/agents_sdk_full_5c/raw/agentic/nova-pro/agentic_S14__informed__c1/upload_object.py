import boto3

s3 = boto3.client('s3')

def upload_object(bucket_name, object_name, file_path):
    with open(file_path, 'rb') as file_data:
        s3.upload_fileobj(file_data, bucket_name, object_name)