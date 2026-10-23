import boto3
import os

def archive_document_to_s3(file_path: str, bucket_name: str, object_name: str):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return {"message": f"Successfully uploaded {file_path} to s3://{bucket_name}/{object_name}"}
    except Exception as e:
        return {"error": str(e)}
