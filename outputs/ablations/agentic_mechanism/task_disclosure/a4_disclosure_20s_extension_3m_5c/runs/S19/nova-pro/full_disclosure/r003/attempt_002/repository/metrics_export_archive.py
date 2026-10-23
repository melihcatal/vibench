import boto3

def archive_metric_snapshot(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    with open(file_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, object_key)
    print(f'Metric snapshot archived at s3://{bucket_name}/{object_key}')

if __name__ == '__main__':
    bucket_name = 'your-s3-bucket'
    object_key = 'path/to/metric_snapshot.json'
    file_path = 'local/path/to/metric_snapshot.json'
    archive_metric_snapshot(bucket_name, object_key, file_path)