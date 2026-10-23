import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions in Amazon S3.

    Args:
        image_path: Path to the original image file
        analysis_results: Dictionary containing all analysis results
        bucket_name: S3 bucket name
        prefix: Optional prefix for S3 object keys

    Returns:
        Dictionary with archive details
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    archive_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if prefix:
        base_prefix = prefix.rstrip("/") + "/"
    else:
        base_prefix = ""

    archive_details = {
        "archive_id": archive_id,
        "timestamp": timestamp,
        "bucket": bucket_name,
        "objects": [],
    }

    try:
        image_filename = os.path.basename(image_path)
        image_key = f"{base_prefix}{archive_id}/original/{image_filename}"

        with open(image_path, "rb") as image_file:
            s3_client.upload_fileobj(image_file, bucket_name, image_key)

        archive_details["objects"].append(
            {
                "key": image_key,
                "type": "original_image",
                "size": os.path.getsize(image_path),
            }
        )

        analysis_key = f"{base_prefix}{archive_id}/analysis/results.json"
        analysis_json = json.dumps(analysis_results, indent=2)

        s3_client.put_object(
            Bucket=bucket_name,
            Key=analysis_key,
            Body=analysis_json.encode("utf-8"),
            ContentType="application/json",
        )

        archive_details["objects"].append(
            {
                "key": analysis_key,
                "type": "analysis_results",
                "size": len(analysis_json),
            }
        )

        summary = analysis_results.get("summary", {})
        if summary and "summary" in summary:
            summary_text = summary.get("summary", "")
            if summary_text:
                summary_key = f"{base_prefix}{archive_id}/summary/summary.txt"
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=summary_key,
                    Body=summary_text.encode("utf-8"),
                    ContentType="text/plain",
                )

                archive_details["objects"].append(
                    {
                        "key": summary_key,
                        "type": "text_summary",
                        "size": len(summary_text),
                    }
                )

        metadata_key = f"{base_prefix}{archive_id}/metadata.json"
        metadata = {
            "archive_id": archive_id,
            "created_at": timestamp,
            "image_filename": image_filename,
            "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
            "provider": "amazon-s3",
            "object_count": len(archive_details["objects"]),
        }

        s3_client.put_object(
            Bucket=bucket_name,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

        archive_details["objects"].append(
            {"key": metadata_key, "type": "metadata", "size": len(json.dumps(metadata))}
        )

        archive_details["success"] = True
        archive_details["metadata"] = metadata

        return archive_details

    except Exception as e:
        raise Exception(f"Amazon S3 archive error: {str(e)}")
