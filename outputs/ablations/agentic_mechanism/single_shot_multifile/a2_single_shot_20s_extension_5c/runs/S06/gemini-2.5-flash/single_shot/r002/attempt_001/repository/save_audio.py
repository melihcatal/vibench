import os
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

def save_audio_to_s3(
    audio_content: bytes,
    bucket_name: str,
    object_name: str,
    content_type: str = "audio/mpeg"
) -> str:
    """
    Uploads audio content to an S3 bucket.
    Returns the S3 object URL if successful, raises an exception otherwise.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=audio_content,
            ContentType=content_type
        )
        location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{object_name}"
        return url
    except ClientError as e:
        raise RuntimeError(f"Failed to upload audio to S3: {e}")

def save_audio_to_local_file(audio_content: bytes, file_path: str) -> None:
    """
    Saves audio content to a local file.
    """
    with open(file_path, "wb") as f:
        f.write(audio_content)
