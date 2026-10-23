import boto3

client = boto3.client("s3")


def image_asset_archive(bucket_name, object_key, file_path):
    client.upload_file(file_path, bucket_name, object_key)
