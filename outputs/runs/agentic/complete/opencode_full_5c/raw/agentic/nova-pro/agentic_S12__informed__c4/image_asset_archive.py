import boto3


def archive_image_assets(bucket_name, file_path, object_name):
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_path, bucket_name, object_name)
