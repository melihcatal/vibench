from __future__ import annotations

import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

from vision_models import (
    ImageLabelResponse,
    ImageDescriptionResponse,
    ImageTextResponse,
    ImageSafetyResponse,
)

AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET", "image-analysis-archive")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")


def get_s3_client() -> boto3.client:
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def _serialize_response(obj) -> dict:
    if hasattr(obj, "__dict__"):
        data = {}
        for k, v in vars(obj).items():
            if isinstance(v, list):
                data[k] = [_serialize_response(item) for item in v]
            elif hasattr(v, "__dict__"):
                data[k] = _serialize_response(v)
            else:
                data[k] = v
        return data
    return obj


def archive_image_analysis(
    image_path: str,
    labels_resp: ImageLabelResponse | None = None,
    description_resp: ImageDescriptionResponse | None = None,
    text_resp: ImageTextResponse | None = None,
    safety_resp: ImageSafetyResponse | None = None,
    summary: str | None = None,
    translated_alt: str | None = None,
    safety_text_result: dict | None = None,
    s3_bucket: str | None = None,
    prefix: str = "analysis",
) -> dict:
    bucket = s3_bucket or AWS_S3_BUCKET
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    key_prefix = f"{prefix}/{base_name}/{timestamp}"

    s3 = get_s3_client()
    uploaded_keys: list[str] = []

    if os.path.exists(image_path):
        image_key = f"{key_prefix}/original/{os.path.basename(image_path)}"
        s3.upload_file(image_path, bucket, image_key)
        uploaded_keys.append(image_key)

    artifacts: dict = {}

    if labels_resp:
        labels_data = _serialize_response(labels_resp)
        labels_json = json.dumps(labels_data, indent=2, default=str)
        labels_key = f"{key_prefix}/labels.json"
        s3.put_object(
            Bucket=bucket,
            Key=labels_key,
            Body=labels_json,
            ContentType="application/json",
        )
        uploaded_keys.append(labels_key)
        artifacts["labels"] = labels_data

    if description_resp:
        desc_data = _serialize_response(description_resp)
        desc_json = json.dumps(desc_data, indent=2, default=str)
        desc_key = f"{key_prefix}/description.json"
        s3.put_object(
            Bucket=bucket, Key=desc_key, Body=desc_json, ContentType="application/json"
        )
        uploaded_keys.append(desc_key)
        artifacts["description"] = desc_data

    if text_resp:
        text_data = _serialize_response(text_resp)
        text_json = json.dumps(text_data, indent=2, default=str)
        text_key = f"{key_prefix}/text.json"
        s3.put_object(
            Bucket=bucket, Key=text_key, Body=text_json, ContentType="application/json"
        )
        uploaded_keys.append(text_key)
        artifacts["text"] = text_data

    if safety_resp:
        safety_data = _serialize_response(safety_resp)
        safety_json = json.dumps(safety_data, indent=2, default=str)
        safety_key = f"{key_prefix}/safety.json"
        s3.put_object(
            Bucket=bucket,
            Key=safety_key,
            Body=safety_json,
            ContentType="application/json",
        )
        uploaded_keys.append(safety_key)
        artifacts["safety"] = safety_data

    if summary:
        summary_key = f"{key_prefix}/summary.txt"
        s3.put_object(
            Bucket=bucket, Key=summary_key, Body=summary, ContentType="text/plain"
        )
        uploaded_keys.append(summary_key)
        artifacts["summary"] = summary

    if translated_alt:
        alt_key = f"{key_prefix}/translated_alt.txt"
        s3.put_object(
            Bucket=bucket, Key=alt_key, Body=translated_alt, ContentType="text/plain"
        )
        uploaded_keys.append(alt_key)
        artifacts["translated_alt"] = translated_alt

    if safety_text_result:
        st_data = json.dumps(safety_text_result, indent=2, default=str)
        st_key = f"{key_prefix}/text_safety.json"
        s3.put_object(
            Bucket=bucket, Key=st_key, Body=st_data, ContentType="application/json"
        )
        uploaded_keys.append(st_key)
        artifacts["text_safety"] = safety_text_result

    manifest = {
        "image_path": image_path,
        "timestamp": timestamp,
        "bucket": bucket,
        "prefix": key_prefix,
        "uploaded_keys": uploaded_keys,
        "artifacts": {k: type(v).__name__ for k, v in artifacts.items()},
    }
    manifest_key = f"{key_prefix}/manifest.json"
    manifest_json = json.dumps(manifest, indent=2)
    s3.put_object(
        Bucket=bucket,
        Key=manifest_key,
        Body=manifest_json,
        ContentType="application/json",
    )
    uploaded_keys.append(manifest_key)

    return {
        "bucket": bucket,
        "prefix": key_prefix,
        "manifest_key": manifest_key,
        "uploaded_keys": uploaded_keys,
        "artifacts": artifacts,
        "manifest": manifest,
    }


def archive_from_summary_result(
    summary_result: dict,
    s3_bucket: str | None = None,
    prefix: str = "analysis",
) -> dict:
    return archive_image_analysis(
        image_path=summary_result.get("image_path", ""),
        labels_resp=summary_result.get("labels"),
        description_resp=summary_result.get("description"),
        text_resp=summary_result.get("text"),
        safety_resp=summary_result.get("safety"),
        summary=summary_result.get("summary"),
        s3_bucket=s3_bucket,
        prefix=prefix,
    )


def list_archived_assets(
    prefix: str = "analysis",
    s3_bucket: str | None = None,
) -> list[dict]:
    bucket = s3_bucket or AWS_S3_BUCKET
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    assets: list[dict] = []
    for obj in response.get("Contents", []):
        if obj["Key"].endswith("/manifest.json"):
            body = s3.get_object(Bucket=bucket, Key=obj["Key"])
            manifest = json.loads(body["Body"].read().decode("utf-8"))
            assets.append(manifest)
    return assets


def delete_archived_assets(
    prefix: str,
    s3_bucket: str | None = None,
) -> int:
    bucket = s3_bucket or AWS_S3_BUCKET
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
    if not keys:
        return 0
    s3.delete_objects(Bucket=bucket, Delete={"Objects": keys})
    return len(keys)


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    from image_summary import summarize_image_full

    result = summarize_image_full(path)
    archive = archive_from_summary_result(result)
    print(f"Archived to s3://{archive['bucket']}/{archive['prefix']}")
    print(f"Uploaded {len(archive['uploaded_keys'])} objects")
