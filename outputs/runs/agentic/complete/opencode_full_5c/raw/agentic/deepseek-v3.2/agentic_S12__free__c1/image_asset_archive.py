import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any
from vision_client import get_aws_s3_credentials
from vision_models import ArchiveMetadata


def archive_image_analysis(
    image_path: str, analysis_results: Dict[str, Any], bucket_name: str
) -> ArchiveMetadata:
    """Archive image-analysis artifacts and derived captions in AWS S3."""
    access_key, secret_key, region = get_aws_s3_credentials()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    # Generate timestamp and object key
    timestamp = datetime.utcnow().isoformat()
    image_filename = os.path.basename(image_path)
    object_key = f"image-analysis/{timestamp}/{image_filename}.json"

    # Prepare metadata
    metadata = {
        "image_path": image_path,
        "image_filename": image_filename,
        "analysis_timestamp": timestamp,
        "analysis_results": analysis_results,
    }

    # Convert to JSON
    metadata_json = json.dumps(metadata, indent=2)

    # Upload to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=metadata_json,
        ContentType="application/json",
        Metadata={"image-filename": image_filename, "analysis-timestamp": timestamp},
    )

    # Also upload the image itself if it exists
    if os.path.exists(image_path):
        image_object_key = f"image-analysis/{timestamp}/{image_filename}"
        with open(image_path, "rb") as image_file:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=image_object_key,
                Body=image_file,
                ContentType="image/jpeg"
                if image_path.lower().endswith(".jpg")
                or image_path.lower().endswith(".jpeg")
                else "image/png",
            )

    return ArchiveMetadata(
        image_path=image_path,
        analysis_results=analysis_results,
        timestamp=timestamp,
        bucket_name=bucket_name,
        object_key=object_key,
    )


def list_archived_analyses(bucket_name: str, prefix: str = "image-analysis/") -> list:
    """List archived image analyses from S3."""
    access_key, secret_key, region = get_aws_s3_credentials()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    archives = []
    if "Contents" in response:
        for obj in response["Contents"]:
            if obj["Key"].endswith(".json"):
                archives.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                    }
                )

    return archives


if __name__ == "__main__":
    # Example usage
    sample_analysis = {
        "labels": [
            {"description": "dog", "score": 0.95},
            {"description": "park", "score": 0.87},
        ],
        "description": "A dog in the park",
        "safety_score": {"flagged": False},
    }

    print("Example archive function - requires AWS credentials and bucket name")
    print(
        "To use: archive_image_analysis('path/to/image.jpg', analysis_results, 'your-bucket-name')"
    )
