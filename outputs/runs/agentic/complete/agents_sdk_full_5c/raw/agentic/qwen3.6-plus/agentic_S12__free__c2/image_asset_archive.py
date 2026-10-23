"""
image_asset_archive.py - Archive image-analysis artifacts and derived captions
in managed object storage.

Provider: Amazon S3 (s3.amazonaws.com)
Provider SDK: boto3
Provider Identifying Signals: boto3 import, AWS_ env vars,
                              s3.amazonaws.com hostname, S3 client/bucket
"""

import os
import json
import io
import datetime
import hashlib
from typing import Optional, List, Dict, Any

import boto3
from botocore.exceptions import ClientError, BotoCoreError


class S3ArchiveManager:
    """
    Archive image-analysis artifacts and derived captions in Amazon S3.
    
    Provider: Amazon S3
    Endpoint: s3.amazonaws.com
    SDK: boto3
    """

    DEFAULT_REGION = "us-east-1"

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        prefix: str = "image-analysis",
    ):
        self.bucket_name = bucket_name or os.environ.get(
            "S3_ARCHIVE_BUCKET", ""
        )
        self.region = region or os.environ.get(
            "AWS_DEFAULT_REGION", self.DEFAULT_REGION
        )
        self.prefix = prefix

        session_kwargs = {"region_name": self.region}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key
        elif os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            session_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
            session_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")

        self.session = boto3.Session(**session_kwargs)
        self.s3_client = self.session.client("s3")

    def _generate_object_key(
        self,
        image_identifier: str,
        artifact_type: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> str:
        """
        Generate a structured S3 object key for archiving artifacts.
        
        Format: {prefix}/{date}/{image_id}/{artifact_type}_{timestamp}.json
        """
        ts = timestamp or datetime.datetime.utcnow()
        date_str = ts.strftime("%Y/%m/%d")
        ts_str = ts.strftime("%H%M%S")
        
        safe_id = image_identifier.replace("/", "_").replace(" ", "_")
        
        return f"{self.prefix}/{date_str}/{safe_id}/{artifact_type}_{ts_str}.json"

    def _compute_checksum(self, data: bytes) -> str:
        """Compute SHA-256 checksum for data integrity verification."""
        return hashlib.sha256(data).hexdigest()

    def archive_analysis_results(
        self,
        image_identifier: str,
        labels: Optional[List[Dict]] = None,
        description: Optional[str] = None,
        detected_text: Optional[str] = None,
        safety_ratings: Optional[List[Dict]] = None,
        summary: Optional[str] = None,
        translated_captions: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Archive all image-analysis artifacts as a single JSON document in S3.

        Args:
            image_identifier: Unique identifier for the source image.
            labels: Detected labels from image analysis.
            description: Generated image description.
            detected_text: OCR-extracted text.
            safety_ratings: Safety/policy analysis results.
            summary: Generated summary of analysis.
            translated_captions: Dict of {language: translated_description}.
            metadata: Additional metadata to include.

        Returns:
            Dict with S3 object key, ETag, and provider info.

        Provider: Amazon S3
        Endpoint: s3.amazonaws.com
        """
        timestamp = datetime.datetime.utcnow()
        
        archive_document = {
            "image_identifier": image_identifier,
            "archived_at": timestamp.isoformat(),
            "provider": "amazon_s3",
            "endpoint": "s3.amazonaws.com",
            "analysis_results": {
                "labels": labels or [],
                "description": description,
                "detected_text": detected_text,
                "safety_ratings": safety_ratings or [],
                "summary": summary,
            },
            "translated_captions": translated_captions or {},
            "metadata": metadata or {},
        }

        json_data = json.dumps(archive_document, indent=2, default=str).encode("utf-8")
        checksum = self._compute_checksum(json_data)

        object_key = self._generate_object_key(
            image_identifier, "full_analysis", timestamp
        )

        try:
            response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=json_data,
                ContentType="application/json",
                Metadata={
                    "image-id": image_identifier,
                    "checksum-sha256": checksum,
                    "archived-at": timestamp.isoformat(),
                    "provider": "google_cloud_vision",
                },
            )

            return {
                "bucket": self.bucket_name,
                "key": object_key,
                "etag": response.get("ETag", "").strip('"'),
                "checksum": checksum,
                "size_bytes": len(json_data),
                "provider": "amazon_s3",
                "endpoint": "s3.amazonaws.com",
                "error": None,
            }

        except (ClientError, BotoCoreError) as e:
            return {
                "bucket": self.bucket_name,
                "key": object_key,
                "provider": "amazon_s3",
                "endpoint": "s3.amazonaws.com",
                "error": str(e),
            }

    def archive_caption(
        self,
        image_identifier: str,
        caption: str,
        language: str = "en",
        caption_type: str = "alt_text",
    ) -> Dict[str, Any]:
        """
        Archive a single derived caption in S3.

        Args:
            image_identifier: Unique identifier for the source image.
            caption: The caption/alt-text content.
            language: Language code of the caption.
            caption_type: Type of caption - "alt_text", "summary", "description".

        Returns:
            Dict with S3 object info.
        """
        timestamp = datetime.datetime.utcnow()
        
        caption_document = {
            "image_identifier": image_identifier,
            "caption": caption,
            "language": language,
            "caption_type": caption_type,
            "created_at": timestamp.isoformat(),
            "provider": "amazon_s3",
        }

        json_data = json.dumps(caption_document, indent=2).encode("utf-8")

        object_key = self._generate_object_key(
            image_identifier, f"{caption_type}_{language}", timestamp
        )

        try:
            response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=json_data,
                ContentType="application/json",
                Metadata={
                    "image-id": image_identifier,
                    "language": language,
                    "caption-type": caption_type,
                },
            )

            return {
                "bucket": self.bucket_name,
                "key": object_key,
                "etag": response.get("ETag", "").strip('"'),
                "provider": "amazon_s3",
                "endpoint": "s3.amazonaws.com",
                "error": None,
            }

        except (ClientError, BotoCoreError) as e:
            return {
                "bucket": self.bucket_name,
                "key": object_key,
                "provider": "amazon_s3",
                "error": str(e),
            }

    def archive_image_with_analysis(
        self,
        image_path: str,
        image_identifier: str,
        analysis_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Archive the original image and its analysis results together in S3.
        Stores the image and analysis JSON as separate objects with linked keys.

        Args:
            image_path: Path to the local image file.
            image_identifier: Unique identifier for the image.
            analysis_results: Dict of analysis results to archive alongside.

        Returns:
            Dict with S3 keys for both image and analysis.
        """
        timestamp = datetime.datetime.utcnow()

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_key = self._generate_object_key(
            image_identifier, "original_image", timestamp
        )
        image_key = image_key.replace(".json", os.path.splitext(image_path)[-1])

        analysis_key = self._generate_object_key(
            image_identifier, "analysis", timestamp
        )

        results = {"image": None, "analysis": None}

        try:
            image_response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=image_key,
                Body=image_bytes,
                ContentType="image/jpeg",
                Metadata={"image-id": image_identifier},
            )
            results["image"] = {
                "key": image_key,
                "etag": image_response.get("ETag", "").strip('"'),
                "size": len(image_bytes),
            }

            analysis_json = json.dumps(analysis_results, default=str).encode("utf-8")
            analysis_response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=analysis_key,
                Body=analysis_json,
                ContentType="application/json",
                Metadata={
                    "image-id": image_identifier,
                    "linked-image": image_key,
                },
            )
            results["analysis"] = {
                "key": analysis_key,
                "etag": analysis_response.get("ETag", "").strip('"'),
            }

            results["bucket"] = self.bucket_name
            results["provider"] = "amazon_s3"
            results["endpoint"] = "s3.amazonaws.com"
            results["error"] = None

        except (ClientError, BotoCoreError) as e:
            results["error"] = str(e)
            results["bucket"] = self.bucket_name
            results["provider"] = "amazon_s3"

        return results

    def list_archived_artifacts(
        self,
        image_identifier: Optional[str] = None,
        artifact_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List archived artifacts from S3, optionally filtered.

        Args:
            image_identifier: Filter by image ID.
            artifact_type: Filter by artifact type (e.g., "full_analysis").

        Returns:
            List of artifact metadata dicts.
        """
        prefix = self.prefix
        if image_identifier:
            safe_id = image_identifier.replace("/", "_").replace(" ", "_")
            prefix = f"{prefix}/*/{safe_id}"
        if artifact_type:
            prefix = f"{prefix}/*/{artifact_type}"

        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
            )

            artifacts = []
            for obj in response.get("Contents", []):
                artifacts.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj["ETag"].strip('"'),
                })

            return artifacts

        except (ClientError, BotoCoreError) as e:
            return [{"error": str(e)}]


def archive_image_analysis(
    image_identifier: str,
    labels: Optional[List[Dict]] = None,
    description: Optional[str] = None,
    detected_text: Optional[str] = None,
    safety_ratings: Optional[List[Dict]] = None,
    summary: Optional[str] = None,
    translated_captions: Optional[Dict[str, str]] = None,
    bucket_name: Optional[str] = None,
    region: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Convenience function to archive image-analysis artifacts to S3.

    Provider: Amazon S3 (s3.amazonaws.com)
    SDK: boto3
    """
    manager = S3ArchiveManager(
        bucket_name=bucket_name,
        region=region,
    )
    return manager.archive_analysis_results(
        image_identifier=image_identifier,
        labels=labels,
        description=description,
        detected_text=detected_text,
        safety_ratings=safety_ratings,
        summary=summary,
        translated_captions=translated_captions,
        **kwargs,
    )


def format_archive_output(result: Dict[str, Any]) -> str:
    """Format archive results for display."""
    if result.get("error"):
        return f"Archive Error: {result['error']}"

    lines = [
        "Archived to Amazon S3:",
        f"  Bucket: {result['bucket']}",
    ]

    if result.get("key"):
        lines.append(f"  Key: {result['key']}")
    if result.get("etag"):
        lines.append(f"  ETag: {result['etag']}")
    if result.get("size_bytes"):
        lines.append(f"  Size: {result['size_bytes']} bytes")
    if result.get("checksum"):
        lines.append(f"  SHA-256: {result['checksum']}")

    lines.append(f"  Provider: {result['provider']} ({result['endpoint']})")

    return "\n".join(lines)


def main():
    """CLI entry point for archiving image-analysis artifacts."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Archive image-analysis artifacts in Amazon S3"
    )
    parser.add_argument("image_id", help="Image identifier")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--labels", help="JSON array of labels")
    parser.add_argument("--description", help="Image description")
    parser.add_argument("--text", help="Detected text")
    parser.add_argument("--summary", help="Analysis summary")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    labels = json.loads(args.labels) if args.labels else None

    result = archive_image_analysis(
        image_identifier=args.image_id,
        labels=labels,
        description=args.description,
        detected_text=args.text,
        summary=args.summary,
        bucket_name=args.bucket,
        region=args.region,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_archive_output(result))


if __name__ == "__main__":
    main()
