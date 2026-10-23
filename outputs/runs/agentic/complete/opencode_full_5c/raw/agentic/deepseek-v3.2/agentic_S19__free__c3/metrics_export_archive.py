import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any
from google.cloud import storage
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def export_and_archive_metrics(
    metric_name: str, window_hours: int = 24, bucket_name: str = None
) -> Dict[str, Any]:
    """Archive exported metric snapshots in managed object storage."""
    if not bucket_name:
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "metrics-archive-bucket")

    monitoring_client = monitoring_v3.MetricServiceClient()
    storage_client = storage.Client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    now = datetime.utcnow()
    start_time = now - timedelta(hours=window_hours)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(now)

    interval.start_time = start_timestamp
    interval.end_time = end_timestamp

    filter_str = f'metric.type = "{metric_name}"'

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 300}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    try:
        results = monitoring_client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        export_data = {
            "export_timestamp": now.isoformat(),
            "metric_name": metric_name,
            "window_hours": window_hours,
            "project_id": project_id,
            "time_series": [],
        }

        for series in results:
            series_data = {
                "metric_type": series.metric.type,
                "metric_labels": dict(series.metric.labels),
                "resource_type": series.resource.type,
                "resource_labels": dict(series.resource.labels),
                "value_type": series.value_type.name,
                "points": [],
            }

            for point in series.points:
                point_data = {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "interval": {
                        "start": point.interval.start_time.ToDatetime().isoformat(),
                        "end": point.interval.end_time.ToDatetime().isoformat(),
                    },
                }

                if point.value.double_value:
                    point_data["value"] = point.value.double_value
                    point_data["value_type"] = "double"
                elif point.value.int64_value:
                    point_data["value"] = point.value.int64_value
                    point_data["value_type"] = "int64"
                elif point.value.string_value:
                    point_data["value"] = point.value.string_value
                    point_data["value_type"] = "string"
                elif point.value.bool_value:
                    point_data["value"] = point.value.bool_value
                    point_data["value_type"] = "bool"
                elif point.value.distribution_value:
                    point_data["value"] = {
                        "count": point.value.distribution_value.count,
                        "mean": point.value.distribution_value.mean,
                        "sum_of_squared_deviation": point.value.distribution_value.sum_of_squared_deviation,
                    }
                    point_data["value_type"] = "distribution"

                series_data["points"].append(point_data)

            export_data["time_series"].append(series_data)

        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = (
            f"metrics_export/{metric_name.replace('/', '_')}/{timestamp_str}.json"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp_file:
            json.dump(export_data, tmp_file, indent=2, default=str)
            tmp_path = tmp_file.name

        try:
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)

            blob.upload_from_filename(tmp_path, content_type="application/json")

            os.unlink(tmp_path)

            archive_info = {
                "export_success": True,
                "archive_location": f"gs://{bucket_name}/{filename}",
                "bucket": bucket_name,
                "filename": filename,
                "metric_name": metric_name,
                "window_hours": window_hours,
                "export_timestamp": now.isoformat(),
                "time_series_count": len(export_data["time_series"]),
                "total_points": sum(
                    len(series["points"]) for series in export_data["time_series"]
                ),
                "blob_size": blob.size,
                "blob_md5_hash": blob.md5_hash,
                "blob_generation": blob.generation,
                "public_url": blob.public_url,
                "signed_url": blob.generate_signed_url(
                    version="v4", expiration=datetime.timedelta(hours=24), method="GET"
                )
                if not blob.public
                else None,
            }

            return archive_info

        except Exception as storage_error:
            os.unlink(tmp_path)
            raise storage_error

    except Exception as e:
        return {
            "export_success": False,
            "error": str(e),
            "metric_name": metric_name,
            "window_hours": window_hours,
            "export_timestamp": now.isoformat(),
        }


def list_archived_exports(
    bucket_name: str = None, metric_name: str = None
) -> List[Dict[str, Any]]:
    """List archived metric exports."""
    if not bucket_name:
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "metrics-archive-bucket")

    storage_client = storage.Client()

    try:
        bucket = storage_client.bucket(bucket_name)

        prefix = None
        if metric_name:
            safe_metric_name = metric_name.replace("/", "_")
            prefix = f"metrics_export/{safe_metric_name}/"

        blobs = bucket.list_blobs(prefix=prefix)

        exports = []
        for blob in blobs:
            if blob.name.endswith(".json"):
                exports.append(
                    {
                        "name": blob.name,
                        "size": blob.size,
                        "updated": blob.updated.isoformat(),
                        "md5_hash": blob.md5_hash,
                        "generation": blob.generation,
                        "public_url": blob.public_url,
                        "storage_class": blob.storage_class,
                        "time_created": blob.time_created.isoformat()
                        if blob.time_created
                        else None,
                    }
                )

        return {
            "bucket": bucket_name,
            "total_exports": len(exports),
            "exports": exports,
            "metric_filter": metric_name,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "metric_filter": metric_name,
        }


import datetime


def cleanup_old_exports(
    bucket_name: str = None, days_to_keep: int = 90
) -> Dict[str, Any]:
    """Clean up old metric exports from storage."""
    if not bucket_name:
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "metrics-archive-bucket")

    storage_client = storage.Client()

    try:
        bucket = storage_client.bucket(bucket_name)
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days_to_keep)

        blobs_to_delete = []
        total_size = 0

        for blob in bucket.list_blobs(prefix="metrics_export/"):
            if blob.time_created and blob.time_created < cutoff_date:
                blobs_to_delete.append(blob)
                total_size += blob.size

        deleted_count = 0
        for blob in blobs_to_delete:
            blob.delete()
            deleted_count += 1

        return {
            "cleanup_success": True,
            "bucket": bucket_name,
            "cutoff_date": cutoff_date.isoformat(),
            "deleted_count": deleted_count,
            "freed_space_bytes": total_size,
            "freed_space_mb": total_size / (1024 * 1024),
        }

    except Exception as e:
        return {
            "cleanup_success": False,
            "error": str(e),
            "bucket": bucket_name,
            "cutoff_date": cutoff_date.isoformat()
            if "cutoff_date" in locals()
            else None,
        }
