import os
import boto3
from botocore.exceptions import NoCredentialsError


def archive_assets(
    image_path: str, analysis: dict, bucket_name: str, prefix: str = "vision-assets"
) -> None:
    """Archive the original image and generated analysis artifacts in Amazon S3.
    Creates a folder structure like PREFIX/image_name/ and stores:
        - original image
        - labels list (labels.json)
        - description (description.txt)
        - OCR lines (ocr.json)
        - safety flag (safety.json)
    """
    s3 = boto3.client("s3")
    # Ensure bucket exists (boto creates on upload if credentials allow)
    try:
        response = s3.upload_file(
            image_path, bucket_name, f"{prefix}/{os.path.basename(image_path)}"
        )
        # store JSON files
        s3.put_object(
            Body=str(analysis.get("labels", "[]")).encode(),
            Bucket=bucket_name,
            Key=f"{prefix}/{os.path.basename(image_path)}/labels.json",
        )
        s3.put_object(
            Body=analysis.get("description", "").encode(),
            Bucket=bucket_name,
            Key=f"{prefix}/{os.path.basename(image_path)}/description.txt",
        )
        s3.put_object(
            Body=str(analysis.get("ocr", "[]")).encode(),
            Bucket=bucket_name,
            Key=f"{prefix}/{os.path.basename(image_path)}/ocr.json",
        )
        s3.put_object(
            Body=str(analysis.get("safe", True)).encode(),
            Bucket=bucket_name,
            Key=f"{prefix}/{os.path.basename(image_path)}/safety.json",
        )
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not configured")
