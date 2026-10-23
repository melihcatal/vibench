import boto3

def archive_to_s3(bucket_name, file_path, object_name=None):
    s3_client = boto3.client('s3')
    if not object_name:
        object_name = file_path
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(e)
        raise

if __name__ == "__main__":
    bucket_name = 'your-bucket-name'
    file_path = 'path-to-your-file'
    archive_to_s3(bucket_name, file_path)