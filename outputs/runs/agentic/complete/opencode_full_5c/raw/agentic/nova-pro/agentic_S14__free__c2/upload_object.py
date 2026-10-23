import boto3


def upload_object(bucket_name, object_key, file_path):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_key)
    print(f"Uploaded {file_path} to {bucket_name}/{object_key}")
