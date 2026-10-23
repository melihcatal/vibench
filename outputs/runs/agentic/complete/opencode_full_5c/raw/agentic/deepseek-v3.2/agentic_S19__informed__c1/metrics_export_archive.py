import os
import json
import gzip
from datetime import datetime
from typing import Dict, Any, Optional, BinaryIO
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
from observability_client import ObservabilityClient
from observability_models import serialize_response


def archive_metrics_to_gcs(
    metrics_data: Dict[str, Any],
    bucket_name: str,
    object_prefix: str = "metrics-export",
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Google Cloud Storage.

    Args:
        metrics_data: Metrics data to archive
        bucket_name: GCS bucket name
        object_prefix: Prefix for object names

    Returns:
        Archive operation results
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    if not os.path.exists(credentials_path):
        raise ValueError(f"Credentials file not found: {credentials_path}")

    storage_client = storage.Client.from_service_account_json(credentials_path)

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    object_name = f"{object_prefix}/{timestamp}/metrics_export.json.gz"

    try:
        bucket = storage_client.bucket(bucket_name)

        json_data = serialize_response(metrics_data)
        compressed_data = gzip.compress(json_data.encode("utf-8"))

        blob = bucket.blob(object_name)
        blob.upload_from_string(
            compressed_data, content_type="application/gzip", predefined_acl="private"
        )

        blob.make_public()
        public_url = blob.public_url

        metadata = {
            "export_timestamp": timestamp,
            "data_size_bytes": len(json_data),
            "compressed_size_bytes": len(compressed_data),
            "compression_ratio": len(json_data) / len(compressed_data)
            if len(compressed_data) > 0
            else 0,
            "content_type": "application/json",
            "compression": "gzip",
        }

        blob.metadata = metadata
        blob.patch()

        return {
            "success": True,
            "bucket": bucket_name,
            "object_name": object_name,
            "public_url": public_url,
            "metadata": metadata,
            "archive_timestamp": timestamp,
            "service_used": "Google Cloud Storage",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "object_name": object_name,
            "service_used": "Google Cloud Storage",
        }


def archive_metrics_to_s3(
    metrics_data: Dict[str, Any],
    bucket_name: str,
    object_prefix: str = "metrics-export",
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Amazon S3.

    Args:
        metrics_data: Metrics data to archive
        bucket_name: S3 bucket name
        object_prefix: Prefix for object names

    Returns:
        Archive operation results
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    s3_client = session.client("s3")

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    object_key = f"{object_prefix}/{timestamp}/metrics_export.json.gz"

    try:
        json_data = serialize_response(metrics_data)
        compressed_data = gzip.compress(json_data.encode("utf-8"))

        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=compressed_data,
            ContentType="application/gzip",
            ContentEncoding="gzip",
            Metadata={
                "export-timestamp": timestamp,
                "data-size-bytes": str(len(json_data)),
                "compressed-size-bytes": str(len(compressed_data)),
                "content-type": "application/json",
            },
        )

        object_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"

        return {
            "success": True,
            "bucket": bucket_name,
            "object_key": object_key,
            "object_url": object_url,
            "region": region,
            "metadata": {
                "export_timestamp": timestamp,
                "data_size_bytes": len(json_data),
                "compressed_size_bytes": len(compressed_data),
                "compression_ratio": len(json_data) / len(compressed_data)
                if len(compressed_data) > 0
                else 0,
            },
            "archive_timestamp": timestamp,
            "service_used": "Amazon S3",
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "object_key": object_key,
            "service_used": "Amazon S3",
        }


def export_and_archive_metrics(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    bucket_name: str,
    storage_provider: str = "gcs",
    dimension_filters: Optional[Dict[str, str]] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Export metrics and archive them to cloud storage.

    Args:
        metric_name: Metric to export
        start_time: Start time window
        end_time: End time window
        bucket_name: Cloud storage bucket name
        storage_provider: "gcs" or "s3"
        dimension_filters: Optional dimension filters
        project_id: Google Cloud project ID (for GCS)

    Returns:
        Combined export and archive results
    """
    client = ObservabilityClient(project_id)

    time_series_list = client.query_time_series(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimension_filters=dimension_filters,
        alignment_period_seconds=300,
    )

    export_data = {
        "export_metadata": {
            "metric_name": metric_name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "export_timestamp": datetime.utcnow().isoformat(),
            "dimension_filters": dimension_filters or {},
            "time_series_count": len(time_series_list),
        },
        "time_series": [],
    }

    from observability_models import ResponseNormalizer

    for ts in time_series_list:
        normalized = ResponseNormalizer.normalize_time_series(ts)
        export_data["time_series"].append(normalized.to_dict())

    if storage_provider.lower() == "gcs":
        archive_result = archive_metrics_to_gcs(
            metrics_data=export_data,
            bucket_name=bucket_name,
            object_prefix=f"metrics/{metric_name.replace('/', '_')}",
        )
    elif storage_provider.lower() == "s3":
        archive_result = archive_metrics_to_s3(
            metrics_data=export_data,
            bucket_name=bucket_name,
            object_prefix=f"metrics/{metric_name.replace('/', '_')}",
        )
    else:
        raise ValueError(f"Unsupported storage provider: {storage_provider}")

    return {
        "export_summary": {
            "metric_name": metric_name,
            "time_window": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
            "time_series_count": len(time_series_list),
            "total_data_points": sum(
                len(ts["points"]) for ts in export_data["time_series"]
            ),
            "export_size_bytes": len(serialize_response(export_data)),
        },
        "archive_result": archive_result,
        "storage_provider": storage_provider,
    }


def create_archive_manifest(
    bucket_name: str, storage_provider: str = "gcs", manifest_prefix: str = "manifests"
) -> Dict[str, Any]:
    """
    Create a manifest of archived metric exports.

    Args:
        bucket_name: Cloud storage bucket name
        storage_provider: "gcs" or "s3"
        manifest_prefix: Prefix for manifest object

    Returns:
        Manifest creation results
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    manifest_name = f"{manifest_prefix}/archive_manifest_{timestamp}.json"

    manifest_data = {
        "created_at": timestamp,
        "bucket": bucket_name,
        "storage_provider": storage_provider,
        "archives": [],
    }

    json_data = json.dumps(manifest_data, indent=2)

    if storage_provider.lower() == "gcs":
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
            )

        storage_client = storage.Client.from_service_account_json(credentials_path)

        try:
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(manifest_name)
            blob.upload_from_string(
                json_data, content_type="application/json", predefined_acl="private"
            )

            return {
                "success": True,
                "manifest_name": manifest_name,
                "bucket": bucket_name,
                "service_used": "Google Cloud Storage",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "manifest_name": manifest_name,
                "service_used": "Google Cloud Storage",
            }

    elif storage_provider.lower() == "s3":
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

        if not access_key or not secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

        s3_client = session.client("s3")

        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=manifest_name,
                Body=json_data,
                ContentType="application/json",
            )

            return {
                "success": True,
                "manifest_name": manifest_name,
                "bucket": bucket_name,
                "region": region,
                "service_used": "Amazon S3",
            }

        except ClientError as e:
            return {
                "success": False,
                "error": str(e),
                "manifest_name": manifest_name,
                "service_used": "Amazon S3",
            }

    else:
        raise ValueError(f"Unsupported storage provider: {storage_provider}")


if __name__ == "__main__":
    from datetime import datetime, timedelta
    import pytz

    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=1)

    result = export_and_archive_metrics(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        bucket_name="my-metrics-archive-bucket",
        storage_provider="gcs",
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Export and archive result: {result['archive_result']['success']}")
    if result["archive_result"]["success"]:
        print(
            f"Archived to: {result['archive_result'].get('public_url', result['archive_result'].get('object_url', 'N/A'))}"
        )
