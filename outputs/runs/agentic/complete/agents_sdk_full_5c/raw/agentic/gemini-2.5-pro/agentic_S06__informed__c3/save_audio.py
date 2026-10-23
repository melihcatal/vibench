import boto3
from botocore.exceptions import NoCredentialsError

def save_audio_to_s3(audio_bytes: bytes, bucket_name: str, object_name: str) -> str:
    """
    Uploads synthesized audio to an S3 bucket.
    Expects AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(
            Body=audio_bytes,
            Bucket=bucket_name,
            Key=object_name,
            ContentType="audio/mpeg"
        )
        s3_path = f"s3://{bucket_name}/{object_name}"
        print(f"Successfully uploaded audio to {s3_path}")
        return s3_path
    except NoCredentialsError:
        print("Credentials not available for AWS S3.")
        raise
    except Exception as e:
        print(f"An error occurred during S3 upload: {e}")
        raise
