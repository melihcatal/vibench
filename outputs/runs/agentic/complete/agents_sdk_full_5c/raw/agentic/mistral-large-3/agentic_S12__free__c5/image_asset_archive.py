import os
import boto3
from botocore.exceptions import NoCredentialsError
from vision_models import VisualAnalysisSummary


def archive_analysis_artifacts(
    image_path: str,
    summary: VisualAnalysisSummary,
    bucket_name: str,
    object_key_prefix: str
) -> str:
    """Archive image-analysis artifacts in AWS S3."""
    s3_client = boto3.client("s3")
    
    # Upload the original image
    image_key = f"{object_key_prefix}/original_image.jpg"
    s3_client.upload_file(image_path, bucket_name, image_key)
    
    # Upload the analysis summary as JSON
    summary_key = f"{object_key_prefix}/analysis_summary.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=summary_key,
        Body=summary.json().encode("utf-8")
    )
    
    return f"s3://{bucket_name}/{object_key_prefix}"