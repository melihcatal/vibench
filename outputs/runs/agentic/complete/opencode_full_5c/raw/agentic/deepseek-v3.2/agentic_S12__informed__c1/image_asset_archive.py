import os
import json
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from datetime import datetime


def image_asset_archive(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions in Amazon S3.

    Args:
        image_path: Path to the original image file
        analysis_results: Dictionary containing analysis results
        bucket_name: S3 bucket name
        prefix: Optional prefix for S3 object keys

    Returns:
        Dictionary containing archive metadata
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)

    # Create object keys
    if prefix:
        image_key = f"{prefix}/images/{timestamp}_{image_filename}"
        results_key = (
            f"{prefix}/analysis/{timestamp}_{os.path.splitext(image_filename)[0]}.json"
        )
    else:
        image_key = f"images/{timestamp}_{image_filename}"
        results_key = f"analysis/{timestamp}_{os.path.splitext(image_filename)[0]}.json"

    try:
        # Upload original image
        with open(image_path, "rb") as image_file:
            s3_client.upload_fileobj(
                image_file,
                bucket_name,
                image_key,
                ExtraArgs={"ContentType": "image/jpeg"},
            )

        # Upload analysis results as JSON
        results_json = json.dumps(analysis_results, indent=2)
        s3_client.put_object(
            Bucket=bucket_name,
            Key=results_key,
            Body=results_json,
            ContentType="application/json",
        )

        # Generate presigned URLs for access
        image_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": image_key},
            ExpiresIn=3600,
        )

        results_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": results_key},
            ExpiresIn=3600,
        )

        return {
            "success": True,
            "image_key": image_key,
            "results_key": results_key,
            "image_url": image_url,
            "results_url": results_url,
            "bucket": bucket_name,
            "timestamp": timestamp,
            "original_filename": image_filename,
        }

    except ClientError as e:
        raise Exception(f"Amazon S3 error: {e.response['Error']['Message']}")
    except FileNotFoundError:
        raise Exception(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Archive failed: {str(e)}")
