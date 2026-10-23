import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def upload_object(
    bucket_name, object_key, file_path=None, data_bytes=None, content_type=None
):
    """
    Upload a file or byte stream to Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        file_path: Path to local file (optional if data_bytes provided)
        data_bytes: Bytes data to upload (optional if file_path provided)
        content_type: MIME type of the content

    Returns:
        dict: Upload result with success flag and metadata
    """
    s3_client = get_s3_client()

    try:
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        if file_path:
            with open(file_path, "rb") as f:
                s3_client.upload_fileobj(
                    f, bucket_name, object_key, ExtraArgs=extra_args
                )
        elif data_bytes:
            s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data_bytes, **extra_args
            )
        else:
            return {
                "success": False,
                "error": "Either file_path or data_bytes must be provided",
            }

        # Get the object URL
        location = s3_client.get_bucket_location(Bucket=bucket_name)[
            "LocationConstraint"
        ]
        if location is None:
            location = "us-east-1"

        url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_key}"

        return {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "url": url,
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
