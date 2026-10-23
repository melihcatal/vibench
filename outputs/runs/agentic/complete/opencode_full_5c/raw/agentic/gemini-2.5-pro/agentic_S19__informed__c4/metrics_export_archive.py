import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def archive_metrics_snapshot(bucket_name: str, object_name: str, data: str):
    """
    Uploads a metric snapshot to an Amazon S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param object_name: Name for the object in the bucket.
    :param data: The string data to upload.
    :return: True if upload was successful, else False.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        print("AWS credentials not found in environment variables.")
        return False

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    try:
        s3_client.put_object(
            Bucket=bucket_name, Key=object_name, Body=data.encode("utf-8")
        )
        print(f"Successfully uploaded {object_name} to {bucket_name}")
        return True
    except FileNotFoundError:
        print("The data to upload was not found.")
        return False
    except (NoCredentialsError, PartialCredentialsError):
        print("Credentials not available or incomplete.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
