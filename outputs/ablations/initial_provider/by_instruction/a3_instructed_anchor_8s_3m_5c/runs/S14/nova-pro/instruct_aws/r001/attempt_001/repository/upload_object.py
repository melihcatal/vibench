import boto3

def upload_object(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    with open(file_path, 'rb') as file:
        s3.upload_fileobj(file, bucket_name, object_key)
    print(f'File uploaded to {bucket_name}/{object_key}')