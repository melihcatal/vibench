"""
Archive image-analysis artifacts and derived captions in managed object storage.
Provider: AWS S3 (s3.us-east-1.amazonaws.com)
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

import boto3
from botocore.exceptions import ClientError

from vision_client import load_aws_config
from vision_models import ImageAnalysisPayload


class S3ArchiveClient:
    """
    Client for archiving image analysis artifacts to AWS S3.
    Uses s3.us-east-1.amazonaws.com endpoint for object storage.
    """

    def __init__(self, bucket_name: Optional[str] = None, region: str = "us-east-1"):
        self.bucket_name = bucket_name or os.environ.get("IMAGE_ARCHIVE_BUCKET", "image-analysis-archive")
        self.region = region
        config = load_aws_config()
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config["aws_access_key_id"],
            aws_secret_access_key=config["aws_secret_access_key"],
            region_name=self.region,
        )

    def _ensure_bucket(self) -> bool:
        """Ensure the archive bucket exists."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            try:
                if self.region == "us-east-1":
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={"LocationConstraint": self.region},
                    )
                return True
            except ClientError as e:
                print(f"Failed to create bucket {self.bucket_name}: {e}")
                return False

    def archive_analysis_result(
        self,
        payload: ImageAnalysisPayload,
        original_image_bytes: Optional[bytes] = None,
        prefix: str = "analysis",
        include_image: bool = True,
    ) -> Dict[str, Any]:
        """
        Archive an image analysis result to AWS S3.

        Stores both the analysis metadata as JSON and optionally the original image.

        Args:
            payload: ImageAnalysisPayload containing analysis results.
            original_image_bytes: Original image bytes to archive.
            prefix: S3 key prefix for the archive.
            include_image: Whether to also upload the original image.

        Returns:
            Dictionary with S3 object keys and archive metadata.
        """
        if not self._ensure_bucket():
            return {"error": "Bucket not available", "provider": "aws_s3"}

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d/%H%M%S")
        run_id = str(uuid.uuid4())[:8]
        base_key = f"{prefix}/{timestamp}/{run_id}"

        result_key = f"{base_key}/analysis_result.json"
        results_dict = payload.to_summary_dict()
        results_dict["archived_at"] = datetime.now(timezone.utc).isoformat()
        results_dict["archive_provider"] = "aws_s3"
        results_dict["s3_endpoint"] = f"s3.{self.region}.amazonaws.com"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=result_key,
            Body=json.dumps(results_dict, indent=2).encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "image_path": payload.image_path or "bytes",
                "labels_count": str(len(payload.labels)),
                "has_description": str(payload.description is not None),
                "safety_flags": str(payload.has_safety_flags()),
            },
        )

        archived_objects = {"analysis_result": f"s3://{self.bucket_name}/{result_key}"}

        if include_image and original_image_bytes:
            image_ext = "jpg"
            if payload.image_path:
                image_ext = os.path.splitext(payload.image_path)[1].lstrip(".") or "jpg"
            image_key = f"{base_key}/original_image.{image_ext}"

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=image_key,
                Body=original_image_bytes,
                ContentType=f"image/{image_ext}",
            )
            archived_objects["original_image"] = f"s3://{self.bucket_name}/{image_key}"

        if payload.description:
            caption_key = f"{base_key}/caption.txt"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=caption_key,
                Body=payload.description.text.encode("utf-8"),
                ContentType="text/plain",
            )
            archived_objects["caption"] = f"s3://{self.bucket_name}/{caption_key}"

        return {
            "archived": True,
            "provider": "aws_s3",
            "bucket": self.bucket_name,
            "endpoint": f"s3.{self.region}.amazonaws.com",
            "objects": archived_objects,
            "base_key": base_key,
            "archived_at": results_dict["archived_at"],
        }

    def archive_batch(
        self,
        payloads: List[ImageAnalysisPayload],
        image_bytes_list: Optional[List[bytes]] = None,
        prefix: str = "batch_analysis",
    ) -> List[Dict[str, Any]]:
        """
        Archive multiple analysis results to AWS S3.

        Args:
            payloads: List of ImageAnalysisPayload objects.
            image_bytes_list: Optional list of original image bytes.
            prefix: S3 key prefix.

        Returns:
            List of archive result dictionaries.
        """
        results = []
        for i, payload in enumerate(payloads):
            image_bytes = image_bytes_list[i] if image_bytes_list and i < len(image_bytes_list) else None
            result = self.archive_analysis_result(
                payload=payload,
                original_image_bytes=image_bytes,
                prefix=prefix,
            )
            results.append(result)
        return results

    def list_archived_items(
        self,
        prefix: str = "analysis",
        max_keys: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List archived analysis items in S3.

        Args:
            prefix: S3 key prefix to filter by.
            max_keys: Maximum number of keys to return.

        Returns:
            List of archived item metadata.
        """
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys,
        )

        items = []
        for obj in response.get("Contents", []):
            items.append({
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "provider": "aws_s3",
                "bucket": self.bucket_name,
            })

        return items


def archive_to_s3(
    payload: ImageAnalysisPayload,
    image_bytes: Optional[bytes] = None,
    bucket_name: Optional[str] = None,
    region: str = "us-east-1",
) -> Dict[str, Any]:
    """
    Convenience function to archive analysis results to AWS S3.

    Args:
        payload: ImageAnalysisPayload to archive.
        image_bytes: Original image bytes.
        bucket_name: S3 bucket name (uses env var if not specified).
        region: AWS region.

    Returns:
        Archive result dictionary.
    """
    client = S3ArchiveClient(bucket_name=bucket_name, region=region)
    return client.archive_analysis_result(
        payload=payload,
        original_image_bytes=image_bytes,
    )


if __name__ == "__main__":
    from detect_image_labels import detect_labels_in_image
    from describe_image import describe_image
    import sys

    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        label_payload = detect_labels_in_image(image_path=img_path)
        result = archive_to_s3(label_payload, image_bytes=img_bytes)
        print(f"Archived: {result.get('archived')}")
        if result.get("objects"):
            for obj_type, s3_uri in result["objects"].items():
                print(f"  {obj_type}: {s3_uri}")
