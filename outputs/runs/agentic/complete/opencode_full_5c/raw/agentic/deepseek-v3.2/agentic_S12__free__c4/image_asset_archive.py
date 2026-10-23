import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions in AWS S3.

    Args:
        image_path: Path to the original image file
        analysis_results: Dictionary containing all analysis results
        bucket_name: S3 bucket name
        prefix: Optional prefix for S3 object keys

    Returns:
        Dictionary containing archive metadata and URLs
    """
    s3_client = boto3.client("s3")

    # Generate timestamp for unique filenames
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)
    base_name = os.path.splitext(image_filename)[0]

    # Create object key with optional prefix
    if prefix:
        object_prefix = f"{prefix.rstrip('/')}/{base_name}_{timestamp}"
    else:
        object_prefix = f"{base_name}_{timestamp}"

    archive_data = {
        "metadata": {
            "original_image": image_filename,
            "archive_timestamp": timestamp,
            "archive_date": datetime.utcnow().isoformat(),
            "analysis_providers": list(analysis_results.keys()),
        },
        "analysis_results": analysis_results,
    }

    # Upload original image
    image_key = f"{object_prefix}/original/{image_filename}"
    try:
        with open(image_path, "rb") as image_file:
            s3_client.upload_fileobj(image_file, bucket_name, image_key)
        image_url = f"s3://{bucket_name}/{image_key}"
    except Exception as e:
        raise Exception(f"Failed to upload image to S3: {e}")

    # Upload analysis results as JSON
    analysis_key = f"{object_prefix}/analysis/results.json"
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=analysis_key,
            Body=json.dumps(archive_data, indent=2),
            ContentType="application/json",
        )
        analysis_url = f"s3://{bucket_name}/{analysis_key}"
    except Exception as e:
        raise Exception(f"Failed to upload analysis results to S3: {e}")

    # Generate public URLs (if bucket is public)
    try:
        image_public_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
        analysis_public_url = f"https://{bucket_name}.s3.amazonaws.com/{analysis_key}"
    except:
        image_public_url = None
        analysis_public_url = None

    return {
        "archive_id": f"{base_name}_{timestamp}",
        "bucket": bucket_name,
        "s3_paths": {"image": image_key, "analysis": analysis_key},
        "s3_urls": {"image": image_url, "analysis": analysis_url},
        "public_urls": {"image": image_public_url, "analysis": analysis_public_url},
        "metadata": archive_data["metadata"],
        "provider": "aws-s3",
    }


def archive_with_metadata(
    image_path: str,
    labels: list,
    description: str,
    text_detections: list,
    safety_scores: dict,
    bucket_name: str,
    custom_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Archive complete image analysis with structured metadata.

    Args:
        image_path: Path to the original image
        labels: Detected labels
        description: Generated description
        text_detections: Detected text
        safety_scores: Safety analysis
        bucket_name: S3 bucket name
        custom_metadata: Additional metadata to include

    Returns:
        Archive information
    """
    analysis_results = {
        "labels": labels,
        "description": description,
        "text_detections": text_detections,
        "safety_scores": safety_scores,
        "custom_metadata": custom_metadata or {},
    }

    return archive_image_analysis(image_path, analysis_results, bucket_name)


if __name__ == "__main__":
    # Example usage
    sample_image_path = "example.jpg"
    sample_analysis = {
        "labels": [{"description": "mountain", "score": 0.95}],
        "description": "A scenic mountain view",
        "text_detections": [],
        "safety_scores": {"is_adult_content": False},
    }

    try:
        # Note: Requires AWS credentials configured
        archive = archive_image_analysis(
            sample_image_path,
            sample_analysis,
            bucket_name="my-image-analysis-bucket",
            prefix="archives/2024",
        )
        print(f"Archive ID: {archive['archive_id']}")
        print(f"Bucket: {archive['bucket']}")
        print(f"Provider: {archive['provider']}")
        print(f"Image S3 path: {archive['s3_paths']['image']}")
    except Exception as e:
        print(f"Error: {e}")
