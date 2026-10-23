import boto3

def archive_document(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f'File {file_path} uploaded to {bucket_name}/{object_key}')
    except Exception as e:
        print(e)
        print('Failed to upload file to S3')