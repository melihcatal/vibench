import boto3

def archive_metrics_export(bucket_name, file_name):
    s3 = boto3.client('s3')
    with open(file_name, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, file_name)