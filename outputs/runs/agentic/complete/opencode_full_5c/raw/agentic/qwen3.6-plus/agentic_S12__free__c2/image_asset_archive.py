import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from image_summary import (
    summarize_visual_analysis,
    VisualAnalysisSummary,
    format_summary_report,
)
from alt_text_translate import alt_text_translate


AWS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET = os.environ.get("VISION_ASSET_ARCHIVE_BUCKET", "image-analysis-archive")
S3_PREFIX = os.environ.get("VISION_ASSET_ARCHIVE_PREFIX", "visual-analysis")

_s3_client = None


def get_s3_client() -> boto3.client:
    global _s3_client

    if _s3_client is not None:
        return _s3_client

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    config = Config(
        retries={"max_attempts": 5, "mode": "adaptive"},
        read_timeout=60,
        connect_timeout=30,
    )

    _s3_client = session.client("s3", config=config)
    return _s3_client


def generate_asset_key(image_path: str, asset_type: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_hash = hashlib.md5(image_path.encode()).hexdigest()[:8]
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    return f"{S3_PREFIX}/{timestamp}/{file_hash}_{base_name}/{asset_type}"


def upload_to_s3(
    bucket: str,
    key: str,
    data: bytes,
    content_type: str = "application/octet-stream",
) -> str:
    client = get_s3_client()

    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        ContentType=content_type,
    )

    return f"s3://{bucket}/{key}"


def image_asset_archive(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    bucket: Optional[str] = None,
    include_translations: bool = True,
    target_languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    source = image_path or "image_bytes"
    target_bucket = bucket or S3_BUCKET

    summary = summarize_visual_analysis(
        image_path=image_path,
        image_bytes=image_bytes,
        include_text=True,
        include_safety=True,
    )

    archive_results = {
        "source": source,
        "bucket": target_bucket,
        "archived_assets": [],
        "errors": [],
        "model": "aws-s3-archive-v3",
    }

    summary_json = json.dumps(
        {
            "image_path": summary.image_path,
            "label_count": summary.label_count,
            "top_labels": summary.top_labels,
            "descriptions": summary.descriptions,
            "text_detected": summary.text_detected,
            "text_snippet": summary.text_snippet,
            "is_safe": summary.is_safe,
            "safety_score": summary.safety_score,
            "unsafe_flags": summary.unsafe_flags,
            "model_providers": summary.model_providers,
        },
        indent=2,
    )

    summary_key = generate_asset_key(source, "summary.json")
    try:
        summary_url = upload_to_s3(
            bucket=target_bucket,
            key=summary_key,
            data=summary_json.encode("utf-8"),
            content_type="application/json",
        )
        archive_results["archived_assets"].append(
            {"type": "summary", "key": summary_key, "url": summary_url}
        )
    except ClientError as e:
        archive_results["errors"].append({"type": "summary", "error": str(e)})

    report_text = format_summary_report(summary)
    report_key = generate_asset_key(source, "report.txt")
    try:
        report_url = upload_to_s3(
            bucket=target_bucket,
            key=report_key,
            data=report_text.encode("utf-8"),
            content_type="text/plain",
        )
        archive_results["archived_assets"].append(
            {"type": "report", "key": report_key, "url": report_url}
        )
    except ClientError as e:
        archive_results["errors"].append({"type": "report", "error": str(e)})

    if include_translations:
        translations = alt_text_translate(
            image_path=image_path,
            image_bytes=image_bytes,
            target_languages=target_languages,
        )

        translations_json = json.dumps(translations, indent=2, ensure_ascii=False)
        translations_key = generate_asset_key(source, "translations.json")
        try:
            translations_url = upload_to_s3(
                bucket=target_bucket,
                key=translations_key,
                data=translations_json.encode("utf-8"),
                content_type="application/json",
            )
            archive_results["archived_assets"].append(
                {
                    "type": "translations",
                    "key": translations_key,
                    "url": translations_url,
                }
            )
        except ClientError as e:
            archive_results["errors"].append({"type": "translations", "error": str(e)})

    if image_path and image_bytes is None:
        with open(image_path, "rb") as f:
            image_data = f.read()
    elif image_bytes:
        image_data = image_bytes
    else:
        image_data = None

    if image_data:
        image_key = generate_asset_key(source, "original.jpg")
        try:
            image_url = upload_to_s3(
                bucket=target_bucket,
                key=image_key,
                data=image_data,
                content_type="image/jpeg",
            )
            archive_results["archived_assets"].append(
                {"type": "original_image", "key": image_key, "url": image_url}
            )
        except ClientError as e:
            archive_results["errors"].append(
                {"type": "original_image", "error": str(e)}
            )

    archive_results["total_assets"] = len(archive_results["archived_assets"])
    archive_results["archive_complete"] = len(archive_results["errors"]) == 0

    return archive_results


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python image_asset_archive.py <image_path> [bucket_name]")
        sys.exit(1)

    bucket = sys.argv[2] if len(sys.argv) > 2 else None
    result = image_asset_archive(image_path=sys.argv[1], bucket=bucket)
    print(json.dumps(result, indent=2))
