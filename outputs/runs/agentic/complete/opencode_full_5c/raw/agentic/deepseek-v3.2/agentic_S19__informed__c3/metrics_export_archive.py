import os
import json
from datetime import datetime
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


def archive_metrics_export(
    metrics_data: Dict[str, Any], bucket_name: str, prefix: str = "metrics-exports"
) -> str:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    s3_client = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"metrics_export_{timestamp}.json"
    s3_key = f"{prefix}/{filename}" if prefix else filename

    try:
        json_data = json.dumps(metrics_data, indent=2, default=str)

        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_data.encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "export-timestamp": timestamp,
                "data-type": "metrics-export",
                "item-count": str(len(metrics_data.get("metrics", []))),
            },
        )

        return f"s3://{bucket_name}/{s3_key}"
    except ClientError as e:
        raise Exception(f"Failed to archive metrics to S3: {str(e)}")


def archive_metric_snapshot(
    snapshot_data: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    s3_client = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    timestamp = datetime.utcnow().isoformat()
    snapshot_id = snapshot_data.get(
        "snapshot_id", f"snapshot_{int(datetime.utcnow().timestamp())}"
    )

    archive_data = {
        "snapshot_id": snapshot_id,
        "timestamp": timestamp,
        "metrics": snapshot_data.get("metrics", []),
        "metadata": snapshot_data.get("metadata", {}),
        "summary": snapshot_data.get("summary", {}),
    }

    filename = f"{snapshot_id}.json"
    s3_key = f"metric-snapshots/{filename}"

    try:
        json_data = json.dumps(archive_data, indent=2, default=str)

        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_data.encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "snapshot-id": snapshot_id,
                "timestamp": timestamp,
                "metric-count": str(len(archive_data["metrics"])),
            },
        )

        return {
            "success": True,
            "s3_uri": f"s3://{bucket_name}/{s3_key}",
            "snapshot_id": snapshot_id,
            "timestamp": timestamp,
            "bucket": bucket_name,
            "key": s3_key,
        }
    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "snapshot_id": snapshot_id,
            "timestamp": timestamp,
        }


def list_metric_archives(bucket_name: str, prefix: str = "metric-snapshots") -> list:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    s3_client = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        archives = []
        for obj in response.get("Contents", []):
            archives.append(
                {
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj["ETag"],
                }
            )

        return archives
    except ClientError as e:
        raise Exception(f"Failed to list metric archives: {str(e)}")
