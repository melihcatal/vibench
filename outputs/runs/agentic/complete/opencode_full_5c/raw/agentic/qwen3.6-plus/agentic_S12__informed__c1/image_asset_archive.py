import json
import os
import io
import datetime
from typing import Optional, List, Dict
import oss2

OSS_DEFAULT_REGION = "oss-cn-hangzhou"
OSS_ENDPOINT_TEMPLATE = "https://oss-{region}.aliyuncs.com"


def get_oss_auth() -> oss2.Auth:
    """Create OSS authentication object from environment variables."""
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required for Alibaba OSS"
        )

    return oss2.Auth(access_key_id, access_key_secret)


def get_oss_bucket(
    bucket_name: str,
    region: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> oss2.Bucket:
    """Create an OSS bucket client for Alibaba Object Storage Service.

    Uses the oss2 SDK to connect to Alibaba Cloud OSS.
    """
    auth = get_oss_auth()

    if endpoint is None:
        region = region or OSS_DEFAULT_REGION
        endpoint = OSS_ENDPOINT_TEMPLATE.format(region=region)

    return oss2.Bucket(auth, endpoint, bucket_name)


def archive_image_analysis_artifacts(
    bucket_name: str,
    image_key: str,
    artifacts: Dict[str, str],
    region: Optional[str] = None,
    endpoint: Optional[str] = None,
    prefix: str = "image-analysis",
) -> dict:
    """Archive image-analysis artifacts and derived captions in Alibaba OSS.

    Uses the oss2 SDK to connect to Alibaba Cloud Object Storage Service (OSS).
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables.

    Args:
        bucket_name: OSS bucket name.
        image_key: Unique identifier for the source image.
        artifacts: Dictionary mapping artifact type to content string.
                   e.g. {"labels": "...", "description": "...", "summary": "..."}
        region: OSS region (e.g. "oss-cn-hangzhou").
        endpoint: Custom OSS endpoint URL.
        prefix: Storage prefix within the bucket.

    Returns:
        Dictionary with archive status and uploaded object keys.
    """
    bucket = get_oss_bucket(bucket_name, region=region, endpoint=endpoint)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base_path = f"{prefix}/{image_key}/{timestamp}"

    uploaded_keys = []
    upload_results = {}

    for artifact_type, content in artifacts.items():
        object_key = f"{base_path}/{artifact_type}.json"

        metadata = {
            "artifact_type": artifact_type,
            "image_key": image_key,
            "archived_at": timestamp,
            "content_type": "application/json",
        }

        content_bytes = json.dumps(
            {"artifact_type": artifact_type, "content": content}
        ).encode("utf-8")

        result = bucket.put_object(
            object_key,
            content_bytes,
            headers={
                "Content-Type": "application/json",
                "x-oss-meta-artifact-type": artifact_type,
                "x-oss-meta-image-key": image_key,
                "x-oss-meta-archived-at": timestamp,
            },
        )

        if result.status == 200:
            uploaded_keys.append(object_key)
            upload_results[artifact_type] = {
                "key": object_key,
                "status": "uploaded",
                "etag": result.etag,
            }
        else:
            upload_results[artifact_type] = {
                "key": object_key,
                "status": "failed",
                "http_status": result.status,
            }

    manifest = {
        "image_key": image_key,
        "archived_at": timestamp,
        "bucket": bucket_name,
        "provider": "Alibaba Object Storage Service",
        "endpoint": bucket.endpoint,
        "artifact_count": len(uploaded_keys),
        "artifacts": upload_results,
    }

    manifest_key = f"{base_path}/_manifest.json"
    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    bucket.put_object(manifest_key, manifest_bytes)
    uploaded_keys.append(manifest_key)

    return manifest


def list_archived_artifacts(
    bucket_name: str,
    image_key: Optional[str] = None,
    prefix: str = "image-analysis",
    region: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> list:
    """List archived image analysis artifacts from Alibaba OSS."""
    bucket = get_oss_bucket(bucket_name, region=region, endpoint=endpoint)

    search_prefix = prefix
    if image_key:
        search_prefix = f"{prefix}/{image_key}"

    objects = []
    for obj in oss2.ObjectIterator(bucket, prefix=search_prefix):
        objects.append(
            {
                "key": obj.key,
                "size": obj.size,
                "last_modified": obj.last_modified,
                "etag": obj.etag,
            }
        )

    return objects


if __name__ == "__main__":
    result = archive_image_analysis_artifacts(
        bucket_name=os.environ.get("OSS_BUCKET_NAME", "my-vision-analysis-bucket"),
        image_key="test-image-001",
        artifacts={
            "labels": json.dumps(["person", "outdoor", "building"]),
            "description": "A person standing in front of a modern building.",
            "safety": json.dumps({"overall_safe": True}),
        },
    )
    print(json.dumps(result, indent=2))
