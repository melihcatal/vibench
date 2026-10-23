import os
import boto3

def record_export_archive(file_content: bytes, bucket_name: str, object_key: str):
    s3_client = boto3.client('s3', 
                             aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
    
    if not all([os.environ.get("AWS_ACCESS_KEY_ID"), os.environ.get("AWS_SECRET_ACCESS_KEY")]):
        raise ValueError("AWS credentials environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not set.")

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        return {"status": "success", "object_key": object_key, "bucket_name": bucket_name}
    except Exception as e:
        print(f"Error archiving file to S3: {e}")
        return {"status": "error", "message": str(e)}
