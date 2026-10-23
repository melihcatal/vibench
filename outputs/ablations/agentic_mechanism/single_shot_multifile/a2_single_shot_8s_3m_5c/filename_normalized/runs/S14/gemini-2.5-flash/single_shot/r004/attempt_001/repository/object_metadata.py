import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def get_object_metadata(
    bucket_name: str,
    object_key: str
) -> dict:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        metadata = {
            "content_type": response.get('ContentType'),
            "content_length": response.get('ContentLength'),
            "last_modified": response.get('LastModified').isoformat() if response.get('LastModified') else None,
            "e_tag": response.get('ETag', '').strip('"'),
            "user_metadata": response.get('Metadata', {})
        }
        return {"status": "success", "object_key": object_key, "metadata": metadata}
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return {"status": "error", "message": f"Object '{object_key}' not found in bucket '{bucket_name}'."}
        return {"status": "error", "message": str(e)}
    except NoCredentialsError:
        return {"status": "error", "message": "AWS credentials not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
