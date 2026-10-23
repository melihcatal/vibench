import boto3


def image_asset_archive(image_path, bucket_name):
    s3 = boto3.client("s3")
    s3.upload_file(image_path, bucket_name, image_path.split("/")[-1])
