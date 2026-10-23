from boto3 import client


def export_archive(bucket_name, file_path):
    s3 = client('s3')
    s3.upload_file(file_path, bucket_name, file_path)
