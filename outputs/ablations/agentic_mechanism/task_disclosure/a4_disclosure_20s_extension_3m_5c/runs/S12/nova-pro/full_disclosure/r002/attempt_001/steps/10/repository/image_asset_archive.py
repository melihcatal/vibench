import boto3

def archive_image_assets(bucket_name, file_path, object_name=None):
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_path
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f'File {file_path} uploaded to {bucket_name}/{object_name}')
    except Exception as e:
        print(e)
        raise

# Example usage:
# archive_image_assets('my-bucket', 'path/to/image.jpg')