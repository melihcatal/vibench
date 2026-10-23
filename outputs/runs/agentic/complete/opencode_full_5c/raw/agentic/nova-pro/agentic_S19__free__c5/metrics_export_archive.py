import boto3

s3_client = boto3.client("s3")


def metrics_export_archive(bucket_name: str, file_path: str):
    with open(file_path, "rb") as data:
        s3_client.upload_fileobj(data, bucket_name, file_path)
