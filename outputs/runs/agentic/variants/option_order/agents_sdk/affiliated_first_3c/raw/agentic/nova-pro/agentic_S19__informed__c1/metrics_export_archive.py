import boto3

def archive_metric_snapshot(bucket_name, object_key, file_path):
    client = boto3.client('s3')
    client.upload_file(file_path, bucket_name, object_key)