
import boto3
import os

# AWS S3 configuration
# It's recommended to manage credentials securely, e.g., using environment variables or IAM roles.
# For demonstration purposes, placeholders are used here.
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "YOUR_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "YOUR_AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")  # e.g., us-east-1
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "your-unique-s3-bucket-name")

def archive_asset(file_path: str, s3_object_name: str):
    """
    Archives an image-analysis artifact or derived caption to AWS S3.

    Args:
        file_path (str): The local path to the file to upload.
        s3_object_name (str): The desired object name (key) in the S3 bucket.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        s3.upload_file(file_path, S3_BUCKET_NAME, s3_object_name)
        print(f"Successfully archived {file_path} to s3://{S3_BUCKET_NAME}/{s3_object_name}")
    except Exception as e:
        print(f"Error archiving {file_path} to S3: {e}")

if __name__ == "__main__":
    # Example usage:
    # Create a dummy artifact file
    dummy_artifact_content = "This is a dummy image analysis artifact."
    dummy_artifact_path = "dummy_artifact.txt"
    with open(dummy_artifact_path, "w") as f:
        f.write(dummy_artifact_content)

    # Archive the dummy artifact
    archive_asset(dummy_artifact_path, "artifacts/dummy_image_analysis.txt")

    # Create a dummy caption file
    dummy_caption_content = "This is a dummy caption for an image."
    dummy_caption_path = "dummy_caption.txt"
    with open(dummy_caption_path, "w") as f:
        f.write(dummy_caption_content)

    # Archive the dummy caption
    archive_asset(dummy_caption_path, "captions/dummy_image_caption.txt")

    # Clean up dummy files
    os.remove(dummy_artifact_path)
    os.remove(dummy_caption_path)
