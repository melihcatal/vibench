import boto3

def archive_metric_snapshots(bucket_name, prefix, local_file_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file_path, bucket_name, prefix + local_file_path.split('/')[-1])
        print(f'Successfully archived {local_file_path} to {bucket_name}')
    except Exception as e:
        print(f'Error archiving {local_file_path}: {e}')

# Example usage:
# archive_metric_snapshots('my-metrics-bucket', 'metrics/', 'path/to/local/metric_snapshot.json')