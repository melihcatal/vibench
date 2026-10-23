import os
import boto3
from botocore.exceptions import NoCredentialsError
from typing import Dict, Any


def archive_analysis_artifacts(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str
) -> str:
    """Archive image-analysis artifacts and derived captions in AWS S3."""
    s3_client = boto3.client("s3")
    
    # Upload the original image
    image_key = f"images/{os.path.basename(image_path)}"
    s3_client.upload_file(image_path, bucket_name, image_key)
    
    # Upload the analysis results
    results_key = f"analysis/{os.path.basename(image_path)}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=results_key,
        Body=str(analysis_results)
    )
    
    return f"s3://{bucket_name}/{results_key}"