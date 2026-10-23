import boto3

def archive_image_assets(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f'File {file_path} uploaded to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

if __name__ == '__main__':
    archive_image_assets('my-image-bucket', 'image-analysis/artifacts/caption.txt', 'path/to/local/caption.txt')