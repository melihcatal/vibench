import boto3


def metrics_export_archive(bucket_name, file_path):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, file_path)
