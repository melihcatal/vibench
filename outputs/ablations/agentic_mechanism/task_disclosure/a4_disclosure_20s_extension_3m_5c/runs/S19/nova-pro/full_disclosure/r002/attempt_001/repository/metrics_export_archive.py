import boto3

def archive_metric_snapshot(bucket_name, object_key, file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f'File {file_path} uploaded to {bucket_name}/{object_key}')
    except Exception as e:
        print(f'Error uploading file: {e}')

# Example usage:
# archive_metric_snapshot('my-metrics-bucket', 'snapshots/2026-09-20/metric-snapshot.json', 'local-metric-snapshot.json')