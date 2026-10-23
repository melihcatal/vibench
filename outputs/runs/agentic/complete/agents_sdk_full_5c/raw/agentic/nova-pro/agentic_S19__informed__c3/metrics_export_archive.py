import boto3

def archive_metrics_export(file_path, bucket_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, os.path.basename(file_path)