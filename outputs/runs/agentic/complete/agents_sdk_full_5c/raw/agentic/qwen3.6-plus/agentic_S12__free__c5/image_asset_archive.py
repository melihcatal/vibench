"""
image_asset_archive.py - Archive image-analysis artifacts and derived captions
in managed object storage using AWS S3.
"""

import json
import io
import os
import uuid
from datetime import datetime, timezone
from typing import Union, List, Optional, Dict, Any

from vision_client import build_s3_client, load_image_bytes
from vision_models import (
    ImageAnalysisResult,
    ImageDescription,
    SafetyVerdict,
    TranslatedText,
)


def _generate_archive_key(prefix: str, image_name: str) -> str:
    """Generate a unique S3 object key for archiving."""
    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    safe_name = os.path.splitext(os.path.basename(image_name))[0].replace(" ", "_")
    return f"{prefix}/{timestamp}/{unique_id}_{safe_name}"


def archive_analysis_result(
    analysis: ImageAnalysisResult,
    bucket: str,
    image_source: Optional[Union[str, bytes]] = None,
    image_name: Optional[str] = None,
    prefix: str = "visual-analysis",
    region: Optional[str] = None,
) -> Dict[str, str]:
    """
    Archive an ImageAnalysisResult and optional source image to AWS S3.

    Args:
        analysis: The ImageAnalysisResult to archive.
        bucket: Target S3 bucket name.
        image_source: Optional path or bytes of the original image to archive.
        image_name: Optional name for the archived image.
        prefix: S3 key prefix for the archive.
        region: AWS region for the S3 client.

    Returns:
        Dictionary mapping artifact type to its S3 object key.
    """
    s3_client = build_s3_client(region)

    if not image_name:
        if isinstance(image_source, str):
            image_name = os.path.basename(image_source)
        else:
            image_name = "image"

    archive_key = _generate_archive_key(prefix, image_name)

    archived = {}

    # Archive the structured analysis result as JSON
    analysis_data = analysis.to_dict()
    analysis_data["archived_at"] = datetime.now(timezone.utc).isoformat()
    analysis_json = json.dumps(analysis_data, indent=2)

    analysis_key = f"{archive_key}/analysis_result.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=analysis_key,
        Body=analysis_json.encode("utf-8"),
        ContentType="application/json",
    )
    archived["analysis"] = f"s3://{bucket}/{analysis_key}"

    # Archive the image if provided
    if image_source is not None:
        image_bytes = load_image_bytes(image_source)
        image_ext = os.path.splitext(image_name)[1] or ".bin"
        image_key = f"{archive_key}/source{image_ext}"
        s3_client.put_object(
            Bucket=bucket,
            Key=image_key,
            Body=image_bytes,
            ContentType="image/*",
        )
        archived["image"] = f"s3://{bucket}/{image_key}"

    # Archive derived captions/descriptions
    if analysis.description:
        caption_key = f"{archive_key}/caption.json"
        caption_data = analysis.description.to_dict()
        s3_client.put_object(
            Bucket=bucket,
            Key=caption_key,
            Body=json.dumps(caption_data, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
        archived["caption"] = f"s3://{bucket}/{caption_key}"

    # Archive translated descriptions if present
    if hasattr(analysis, "translations") and analysis.translations:
        for translation in analysis.translations:
            if isinstance(translation, TranslatedText):
                trans_key = (
                    f"{archive_key}/translation_{translation.target_language}.json"
                )
                s3_client.put_object(
                    Bucket=bucket,
                    Key=trans_key,
                    Body=json.dumps(translation.to_dict(), indent=2).encode("utf-8"),
                    ContentType="application/json",
                )
                archived[f"translation_{translation.target_language}"] = (
                    f"s3://{bucket}/{trans_key}"
                )

    # Archive safety verdict
    if analysis.safety:
        safety_key = f"{archive_key}/safety.json"
        s3_client.put_object(
            Bucket=bucket,
            Key=safety_key,
            Body=json.dumps(analysis.safety.to_dict(), indent=2).encode("utf-8"),
            ContentType="application/json",
        )
        archived["safety"] = f"s3://{bucket}/{safety_key}"

    return archived


def archive_batch_results(
    results: List[Dict[str, Any]],
    bucket: str,
    batch_name: str = "batch",
    region: Optional[str] = None,
) -> str:
    """
    Archive multiple analysis results as a batch manifest to AWS S3.

    Args:
        results: List of dictionaries containing analysis results and metadata.
        bucket: Target S3 bucket name.
        batch_name: Name for the batch archive.
        region: AWS region for the S3 client.

    Returns:
        S3 URI of the batch manifest file.
    """
    s3_client = build_s3_client(region)

    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    unique_id = uuid.uuid4().hex[:8]
    safe_batch = batch_name.replace(" ", "_")

    manifest_key = f"{safe_batch}/{timestamp}/{unique_id}_manifest.json"
    manifest_data = {
        "batch_name": batch_name,
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "result_count": len(results),
        "results": results,
    }

    s3_client.put_object(
        Bucket=bucket,
        Key=manifest_key,
        Body=json.dumps(manifest_data, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    return f"s3://{bucket}/{manifest_key}"


def retrieve_archived_analysis(
    bucket: str,
    object_key: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve a previously archived analysis result from AWS S3.

    Args:
        bucket: S3 bucket name.
        object_key: S3 object key for the analysis JSON.
        region: AWS region for the S3 client.

    Returns:
        Parsed analysis result dictionary.
    """
    s3_client = build_s3_client(region)

    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    body = response["Body"].read().decode("utf-8")
    return json.loads(body)


if __name__ == "__main__":
    import sys
    from vision_models import (
        ImageAnalysisResult,
        ImageLabel,
        ImageDescription,
        DetectedText,
        SafetyVerdict,
    )

    if len(sys.argv) < 2:
        print("Usage: python image_asset_archive.py <bucket_name> [image_path]")
        sys.exit(1)

    bucket = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else None

    sample = ImageAnalysisResult(
        labels=[
            ImageLabel(name="Dog", confidence=0.95),
            ImageLabel(name="Park", confidence=0.82),
        ],
        description=ImageDescription(
            text="A golden retriever sitting on grass in a park.",
            model_id="gpt-4o",
        ),
        detected_texts=[
            DetectedText(text="Dog Park", confidence=0.91),
        ],
        safety=SafetyVerdict(is_safe=True, details="No unsafe content detected."),
    )

    archived = archive_analysis_result(
        analysis=sample,
        bucket=bucket,
        image_source=image_path,
    )
    for artifact_type, s3_uri in archived.items():
        print(f"{artifact_type}: {s3_uri}")
