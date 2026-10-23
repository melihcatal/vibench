import boto3

def upload_to_s3(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_key)
        print(f'File uploaded successfully to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

if __name__ == '__main__':
    bucket_name = 'your-bucket-name'
    object_key = 'your-object-key'
    file_path = 'path-to-your-file'
    upload_to_s3(bucket_name, object_key, file_path)