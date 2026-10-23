import os
import boto3
from botocore.exceptions import NoCredentialsError

def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration: int = 3600
) -> dict:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return {"status": "success", "url": response}
    except NoCredentialsError:
        return {"status": "error", "message": "AWS credentials not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
