import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Optional


def upload_to_s3(
    file_path: str, bucket_name: str, object_name: Optional[str] = None
) -> str:
    """Uploads an image or analysis artifact to Amazon S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    if not object_name:
        object_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except (NoCredentialsError, ClientError) as e:
        raise Exception(f"Failed to upload file to S3: {str(e)}")


def archive_image_analysis(
    image_path: str, analysis_results: dict, bucket_name: str
) -> str:
    """Archives image analysis artifacts and derived captions in Amazon S3."""
    import json
    import tempfile

    # Upload the original image
    image_url = upload_to_s3(image_path, bucket_name)

    # Create a temporary file for the analysis results
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as temp_file:
        json.dump(analysis_results, temp_file)
        temp_file_path = temp_file.name

    # Upload the analysis results
    analysis_url = upload_to_s3(
        temp_file_path, bucket_name, f"analysis_{os.path.basename(image_path)}.json"
    )

    # Clean up
    os.unlink(temp_file_path)

    return {"image_url": image_url, "analysis_url": analysis_url}
