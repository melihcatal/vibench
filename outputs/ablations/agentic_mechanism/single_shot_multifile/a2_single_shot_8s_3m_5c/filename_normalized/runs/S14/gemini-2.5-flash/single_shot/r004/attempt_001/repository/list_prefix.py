import os
import boto3
from botocore.exceptions import NoCredentialsError

def list_objects_with_prefix(
    bucket_name: str,
    prefix: str = ''
) -> dict:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        objects = []
        if 'Contents' in response:
            for item in response['Contents']:
                objects.append({
                    "key": item['Key'],
                    "last_modified": item['LastModified'].isoformat(),
                    "size": item['Size'],
                    "e_tag": item['ETag'].strip('"')
                })
        return {"status": "success", "prefix": prefix, "objects": objects}
    except NoCredentialsError:
        return {"status": "error", "message": "AWS credentials not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
