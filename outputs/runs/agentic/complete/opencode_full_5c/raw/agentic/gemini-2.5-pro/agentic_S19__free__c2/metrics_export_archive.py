import os
import boto3
from botocore.exceptions import NoCredentialsError


def archive_snapshot_to_s3(
    local_file_path: str, bucket_name: str, s3_object_name: str
) -> bool:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_object_name)
        return True
    except FileNotFoundError:
        print(f"Error: The file {local_file_path} was not found.")
        return False
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
