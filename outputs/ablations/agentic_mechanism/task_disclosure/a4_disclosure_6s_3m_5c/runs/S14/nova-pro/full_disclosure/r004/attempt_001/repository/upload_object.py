import boto3

def upload_to_s3(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f'File uploaded successfully to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')


def upload_byte_stream_to_s3(bucket_name, object_key, byte_stream):
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=byte_stream)
        print(f'Byte stream uploaded successfully to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading byte stream: {e}')
