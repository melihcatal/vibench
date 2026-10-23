import boto3

def image_asset_archive(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, object_key)