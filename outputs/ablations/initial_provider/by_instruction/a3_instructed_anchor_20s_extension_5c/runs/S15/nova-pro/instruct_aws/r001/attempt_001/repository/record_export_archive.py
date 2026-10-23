import boto3

def archive_record(bucket_name, file_path, object_name=None):
    if not object_name:
        object_name = file_path
    s3 = boto3.client('s3')
    response = s3.upload_file(file_path, bucket_name, object_name)
    return response