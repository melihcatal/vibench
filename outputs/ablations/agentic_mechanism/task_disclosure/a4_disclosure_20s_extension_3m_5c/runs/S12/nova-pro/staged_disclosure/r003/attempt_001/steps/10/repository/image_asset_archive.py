import boto3

def upload_to_s3(bucket_name, file_path, object_name=None):
    if object_name is None:
        object_name = file_path
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Upload Successful: {object_name}")
    except Exception as e:
        print(e)
        raise

if __name__ == "__main__":
    bucket_name = 'your-bucket-name'
    file_path = 'path-to-your-file'
    upload_to_s3(bucket_name, file_path)