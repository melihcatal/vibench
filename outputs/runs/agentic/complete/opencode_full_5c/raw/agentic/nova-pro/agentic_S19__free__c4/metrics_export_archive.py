import boto3


def metrics_export_archive(bucket_name: str, file_name: str):
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_name, bucket_name, file_name)
