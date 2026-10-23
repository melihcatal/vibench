import os
import json
import time
import gzip
import io
from typing import Any

import boto3
from botocore.exceptions import ClientError

from observability_models import MetricSnapshot
from observability_client import serialize_snapshot, deserialize_snapshot

S3_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_s3_client(
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    region: str | None = None,
) -> boto3.client:
    aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = aws_secret_access_key or os.environ.get(
        "AWS_SECRET_ACCESS_KEY", ""
    )
    region = region or os.environ.get("AWS_DEFAULT_REGION", S3_DEFAULT_REGION)
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )
    return session.client("s3")


def archive_snapshot_to_s3(
    snapshot: MetricSnapshot,
    bucket: str,
    key_prefix: str = "metric-snapshots",
    compress: bool = True,
    s3_client: boto3.client | None = None,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    if s3_client is None:
        s3_client = get_s3_client()
    timestamp = snapshot.created_at or int(time.time())
    date_prefix = time.strftime("%Y/%m/%d", time.gmtime(timestamp))
    file_ext = ".json.gz" if compress else ".json"
    object_key = f"{key_prefix}/{date_prefix}/{snapshot.snapshot_id}{file_ext}"
    snapshot_json = serialize_snapshot(snapshot)
    if compress:
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(snapshot_json.encode("utf-8"))
        body = buf.getvalue()
        content_encoding = "gzip"
        content_type = "application/gzip"
    else:
        body = snapshot_json.encode("utf-8")
        content_encoding = None
        content_type = "application/json"
    upload_kwargs: dict[str, Any] = {
        "Bucket": bucket,
        "Key": object_key,
        "Body": body,
        "ContentType": content_type,
    }
    if content_encoding:
        upload_kwargs["ContentEncoding"] = content_encoding
    if metadata:
        upload_kwargs["Metadata"] = metadata
    else:
        upload_kwargs["Metadata"] = {
            "metric-name": snapshot.metric_name,
            "snapshot-id": snapshot.snapshot_id,
        }
    response = s3_client.put_object(**upload_kwargs)
    return {
        "bucket": bucket,
        "key": object_key,
        "snapshot_id": snapshot.snapshot_id,
        "size_bytes": len(body),
        "compressed": compress,
        "etag": response.get("ETag", ""),
        "timestamp": timestamp,
    }


def archive_snapshots_batch(
    snapshots: list[MetricSnapshot],
    bucket: str,
    key_prefix: str = "metric-snapshots",
    compress: bool = True,
    s3_client: boto3.client | None = None,
) -> list[dict[str, Any]]:
    results = []
    for snapshot in snapshots:
        result = archive_snapshot_to_s3(
            snapshot=snapshot,
            bucket=bucket,
            key_prefix=key_prefix,
            compress=compress,
            s3_client=s3_client,
        )
        results.append(result)
    return results


def retrieve_snapshot_from_s3(
    bucket: str,
    key: str,
    s3_client: boto3.client | None = None,
) -> MetricSnapshot:
    if s3_client is None:
        s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read()
    content_encoding = response.get("ContentEncoding", "")
    if content_encoding == "gzip" or key.endswith(".gz"):
        body = gzip.decompress(body)
    snapshot_json = body.decode("utf-8")
    return deserialize_snapshot(snapshot_json)


def list_archived_snapshots(
    bucket: str,
    key_prefix: str = "metric-snapshots",
    s3_client: boto3.client | None = None,
) -> list[dict[str, Any]]:
    if s3_client is None:
        s3_client = get_s3_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    objects = []
    for page in paginator.paginate(Bucket=bucket, Prefix=key_prefix):
        for obj in page.get("Contents", []):
            objects.append(
                {
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj.get("ETag", ""),
                }
            )
    return objects


def delete_archived_snapshot(
    bucket: str,
    key: str,
    s3_client: boto3.client | None = None,
) -> bool:
    if s3_client is None:
        s3_client = get_s3_client()
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def create_bucket_if_not_exists(
    bucket: str,
    region: str | None = None,
    s3_client: boto3.client | None = None,
) -> bool:
    if s3_client is None:
        s3_client = get_s3_client()
    region = region or os.environ.get("AWS_DEFAULT_REGION", S3_DEFAULT_REGION)
    try:
        s3_client.head_bucket(Bucket=bucket)
        return True
    except ClientError:
        try:
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket)
            else:
                s3_client.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            return True
        except ClientError:
            return False


if __name__ == "__main__":
    bucket = os.environ.get("S3_ARCHIVE_BUCKET", "my-metrics-archive")
    prefix = os.environ.get("S3_ARCHIVE_PREFIX", "metric-snapshots")
    s3 = get_s3_client()
    archived = list_archived_snapshots(bucket, prefix, s3)
    print(f"Found {len(archived)} archived snapshots in s3://{bucket}/{prefix}")
    for obj in archived[:5]:
        print(f"  {obj['key']} ({obj['size']} bytes)")
