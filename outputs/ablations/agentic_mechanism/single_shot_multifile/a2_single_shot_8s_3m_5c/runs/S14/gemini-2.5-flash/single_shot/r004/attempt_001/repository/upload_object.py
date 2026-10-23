import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_object(
    bucket_name: str,
    object_key: str,
    file_content: bytes
) -> dict:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        return {"status": "success", "object_key": object_key, "bucket_name": bucket_name}
    except NoCredentialsError:
        return {"status": "error", "message": "AWS credentials not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
