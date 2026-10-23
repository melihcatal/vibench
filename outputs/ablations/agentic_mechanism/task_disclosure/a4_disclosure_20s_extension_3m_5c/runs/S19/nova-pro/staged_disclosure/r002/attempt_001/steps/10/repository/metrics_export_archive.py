import boto3

def archive_metric_snapshots(bucket_name, local_directory):
    s3 = boto3.client('s3')
    for file_name in os.listdir(local_directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(local_directory, file_name)
            s3.upload_file(file_path, bucket_name, file_name)
            print(f'Archived {file_name} to {bucket_name}')

if __name__ == '__main__':
    bucket_name = 'your-s3-bucket-name'
    local_directory = '/path/to/local/directory'
    archive_metric_snapshots(bucket_name, local_directory)