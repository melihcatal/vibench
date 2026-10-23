import boto3

def archive_metric_snapshots(bucket_name, local_file_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file_path, bucket_name, local_file_path)
        print(f'File {local_file_path} uploaded to {bucket_name}.')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    archive_metric_snapshots('your-bucket-name', 'path/to/your/local/file.txt')