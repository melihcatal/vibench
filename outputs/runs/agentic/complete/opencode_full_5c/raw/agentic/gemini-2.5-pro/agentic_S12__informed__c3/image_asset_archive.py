import os
import boto3
import json
from botocore.exceptions import NoCredentialsError


def archive_to_s3(bucket_name: str, object_name: str, data: dict, image_path: str):
    """
    Archives analysis data and the original image to an Amazon S3 bucket.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        # Upload JSON data
        json_object_name = f"{object_name}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=json_object_name,
            Body=json.dumps(data, indent=2),
            ContentType="application/json",
        )
        print(f"Successfully uploaded {json_object_name} to {bucket_name}")

        # Upload image file
        image_object_name = f"{object_name}_{os.path.basename(image_path)}"
        s3_client.upload_file(image_path, bucket_name, image_object_name)
        print(f"Successfully uploaded {image_object_name} to {bucket_name}")

    except NoCredentialsError:
        print("Credentials not available. Please configure AWS credentials.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return True
