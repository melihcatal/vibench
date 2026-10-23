"""
image_asset_archive.py - Archive image-analysis artifacts and derived captions
in managed object storage using Amazon S3 (boto3 SDK).

Provider: Amazon S3
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from vision_models import (
    ImageDescription,
    LabelDetectionResponse,
    SafetyScoreResponse,
    TextDetectionResponse,
)


class S3ArchiveManager:
    """Manages archiving of image analysis artifacts to Amazon S3."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        region_name: str = "us-east-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        prefix: str = "image-analysis",
    ) -> None:
        self._bucket_name = bucket_name or os.environ.get(
            "IMAGE_ARCHIVE_S3_BUCKET", "vision-analysis-artifacts"
        )
        self._prefix = prefix
        self._region_name = region_name

        session_kwargs: Dict[str, Any] = {"region_name": region_name}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key

        self._s3_client = boto3.client("s3", **session_kwargs)

    def _make_object_key(self, image_identifier: str, artifact_type: str) -> str:
        """Build an S3 object key for a given artifact."""
        ts = datetime.datetime.utcnow().strftime("%Y/%m/%d/%H%M%S")
        # Hash the identifier to create a stable short key segment
        hash_id = hashlib.md5(image_identifier.encode()).hexdigest()[:12]
        return f"{self._prefix}/{ts}/{hash_id}/{artifact_type}.json"

    def upload_artifact(
        self,
        image_identifier: str,
        artifact_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, str]] = None,
    ) -> str:
        """Upload a single analysis artifact JSON to S3.

        Args:
            image_identifier: Unique identifier for the source image.
            artifact_type: Type label (e.g., "labels", "description", "text", "safety", "caption").
            data: The artifact data to serialize as JSON.
            metadata: Optional S3 user metadata.

        Returns:
            The S3 object key that was written.
        """
        key = self._make_object_key(image_identifier, artifact_type)

        body = json.dumps(data, indent=2, default=str)

        upload_kwargs: Dict[str, Any] = {
            "Bucket": self._bucket_name,
            "Key": key,
            "Body": body,
            "ContentType": "application/json",
        }

        if metadata:
            upload_kwargs["Metadata"] = metadata
        else:
            upload_kwargs["Metadata"] = {
                "image-identifier": image_identifier,
                "artifact-type": artifact_type,
                "archived-at": datetime.datetime.utcnow().isoformat(),
                "provider": "amazon-s3",
            }

        self._s3_client.put_object(**upload_kwargs)
        return key

    def archive_full_analysis(
        self,
        image_identifier: str,
        image_url: Optional[str] = None,
        label_response: Optional[LabelDetectionResponse] = None,
        description_response: Optional[ImageDescription] = None,
        text_response: Optional[TextDetectionResponse] = None,
        safety_response: Optional[SafetyScoreResponse] = None,
        translated_captions: Optional[Dict[str, str]] = None,
        summary: Optional[str] = None,
    ) -> List[str]:
        """Archive a complete set of analysis artifacts to S3.

        Args:
            image_identifier: Unique identifier for the source image.
            image_url: The original image URL (for reference).
            label_response: Label detection results.
            description_response: Image description results.
            text_response: OCR text detection results.
            safety_response: Safety scoring results.
            translated_captions: Dict of translated alt texts by language.
            summary: Natural-language summary from image_summary.py.

        Returns:
            List of S3 object keys written.
        """
        keys: List[str] = []

        # Archive labels
        if label_response:
            labels_data = {
                "labels": [
                    {
                        "label": l.label,
                        "confidence": l.confidence,
                        "mid": l.mid,
                    }
                    for l in label_response.labels
                ],
                "raw_response": label_response.raw_response,
            }
            key = self.upload_artifact(
                image_identifier, "labels", labels_data,
                metadata={"image-url": image_url or "local-file"}
            )
            keys.append(key)

        # Archive description
        if description_response:
            desc_data = {
                "description": description_response.description,
                "confidence": description_response.confidence,
                "topics": description_response.topics,
            }
            key = self.upload_artifact(
                image_identifier, "description", desc_data
            )
            keys.append(key)

        # Archive text detection
        if text_response:
            text_data = {
                "full_text": text_response.full_text,
                "texts": [
                    {
                        "text": t.text,
                        "confidence": t.confidence,
                        "block_type": t.block_type,
                    }
                    for t in text_response.texts
                ],
            }
            key = self.upload_artifact(image_identifier, "text", text_data)
            keys.append(key)

        # Archive safety
        if safety_response:
            safety_data = {
                "is_safe": safety_response.is_safe,
                "flagged_categories": safety_response.flagged_categories,
                "ratings": [
                    {
                        "category": r.category,
                        "likelihood": r.likelihood,
                        "likelihood_score": r.likelihood_score,
                    }
                    for r in safety_response.ratings
                ],
            }
            key = self.upload_artifact(image_identifier, "safety", safety_data)
            keys.append(key)

        # Archive translated captions
        if translated_captions:
            caption_data = {
                "translations": translated_captions,
            }
            key = self.upload_artifact(
                image_identifier, "translated_captions", caption_data
            )
            keys.append(key)

        # Archive summary
        if summary:
            summary_data = {
                "summary": summary,
            }
            key = self.upload_artifact(
                image_identifier, "summary", summary_data
            )
            keys.append(key)

        return keys

    def ensure_bucket_exists(self) -> bool:
        """Create the S3 bucket if it does not already exist."""
        try:
            self._s3_client.head_bucket(Bucket=self._bucket_name)
            return True
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                self._s3_client.create_bucket(
                    Bucket=self._bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": self._region_name}
                    if self._region_name != "us-east-1"
                    else {},
                )
                return True
            raise

    def list_archived_artifacts(
        self, image_identifier: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List archived artifact keys in S3."""
        prefix = self._prefix
        if image_identifier:
            hash_id = hashlib.md5(image_identifier.encode()).hexdigest()[:12]
            prefix = f"{self._prefix}/*/{hash_id}"

        paginator = self._s3_client.get_paginator("list_objects_v2")
        artifacts = []
        for page in paginator.paginate(Bucket=self._bucket_name, Prefix=prefix):
            for obj in page.get("Contents", []):
                artifacts.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                })
        return artifacts


def archive_analysis(
    image_identifier: str,
    image_url: Optional[str] = None,
    label_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescription] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyScoreResponse] = None,
    translated_captions: Optional[Dict[str, str]] = None,
    summary: Optional[str] = None,
    bucket_name: Optional[str] = None,
) -> List[str]:
    """High-level convenience function to archive a full analysis to S3."""
    manager = S3ArchiveManager(bucket_name=bucket_name)
    manager.ensure_bucket_exists()
    return manager.archive_full_analysis(
        image_identifier=image_identifier,
        image_url=image_url,
        label_response=label_response,
        description_response=description_response,
        text_response=text_response,
        safety_response=safety_response,
        translated_captions=translated_captions,
        summary=summary,
    )


def format_archive_report(
    image_identifier: str, keys: List[str]
) -> str:
    """Format a human-readable archive report."""
    lines = [
        "=== Image Asset Archive Report (Amazon S3) ===",
        "",
        f"Image Identifier: {image_identifier}",
        f"Artifacts Archived: {len(keys)}",
        "",
        "S3 Object Keys:",
    ]
    for k in keys:
        lines.append(f"  s3://{os.environ.get('IMAGE_ARCHIVE_S3_BUCKET', 'vision-analysis-artifacts')}/{k}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo: archive sample analysis data
    sample_labels = LabelDetectionResponse(
        labels=[],
        raw_response={"provider": "google-cloud-vision"},
    )
    sample_desc = ImageDescription(
        description="A scenic mountain landscape with a clear blue lake.",
        confidence=0.93,
        topics=["mountain", "lake", "landscape"],
    )

    try:
        keys = archive_analysis(
            image_identifier="demo-image-001",
            image_url="https://example.com/demo.jpg",
            label_response=sample_labels,
            description_response=sample_desc,
            summary="The image depicts a mountain landscape.",
            translated_captions={"es": "Un paisaje montañoso.", "fr": "Un paysage montagneux."},
        )
        print(format_archive_report("demo-image-001", keys))
    except ClientError as e:
        print(f"S3 error: {e}")
    except Exception as e:
        print(f"Archive error: {e}")
