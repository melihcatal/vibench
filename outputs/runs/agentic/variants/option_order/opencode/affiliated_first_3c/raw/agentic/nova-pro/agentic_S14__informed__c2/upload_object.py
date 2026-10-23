import boto3


def upload_object(bucket_name, object_key, file_path):
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_path, bucket_name, object_key)
    print(f"Uploaded {file_path} to {bucket_name}/{object_key}")
