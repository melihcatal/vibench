import boto3

def archive_metric_snapshot(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f'File {file_path} uploaded to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

if __name__ == '__main__':
    archive_metric_snapshot('your-bucket-name', 'your-object-key', 'path-to-your-file')