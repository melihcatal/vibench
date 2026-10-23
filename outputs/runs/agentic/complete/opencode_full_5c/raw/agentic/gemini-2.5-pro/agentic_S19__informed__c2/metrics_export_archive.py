import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from observability_models import ArchiveRequest


def metrics_export_archive(request: ArchiveRequest) -> dict:
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"success": False, "error": f"AWS credentials not found: {e}"}

    try:
        # Serialize data to JSON string if it's not already bytes or a string
        if isinstance(request.data, (dict, list)):
            archive_content = json.dumps(request.data, indent=2).encode("utf-8")
        elif isinstance(request.data, str):
            archive_content = request.data.encode("utf-8")
        else:
            archive_content = request.data

        s3_client.put_object(
            Bucket=request.bucket_name, Key=request.object_name, Body=archive_content
        )

        return {
            "success": True,
            "bucket": request.bucket_name,
            "object_name": request.object_name,
        }
    except ClientError as e:
        return {
            "success": False,
            "error": f"S3 ClientError: {e.response['Error']['Message']}",
        }
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {e}"}
