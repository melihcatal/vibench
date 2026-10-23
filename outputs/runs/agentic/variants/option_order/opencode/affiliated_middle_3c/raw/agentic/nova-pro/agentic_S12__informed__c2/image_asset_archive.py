import os
import boto3

# Initialize the client
client = boto3.client("s3")


def image_asset_archive(bucket_name, object_name, file_path):
    client.upload_file(file_path, bucket_name, object_name)
