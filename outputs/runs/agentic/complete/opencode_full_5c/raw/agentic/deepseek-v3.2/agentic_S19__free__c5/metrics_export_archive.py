import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any
from google.cloud import storage
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def export_metrics_to_storage(
    metric_name: str, window_hours: int = 24, bucket_name: str = None
) -> Dict[str, Any]:
    """Export metric snapshots to Google Cloud Storage."""

    monitoring_client = monitoring_v3.MetricServiceClient()
    storage_client = storage.Client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    if not bucket_name:
        bucket_name = f"{project_id}-metrics-archive"

    end_time = datetime.now()
    start_time = end_time - timedelta(hours=window_hours)

    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)
    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    filter_str = f'metric.type = "{metric_name}"'

    try:
        results = monitoring_client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "metric_name": metric_name,
            "window_hours": window_hours,
            "project_id": project_id,
            "time_series": [],
        }

        for series in results:
            series_data = {
                "metric": {
                    "type": series.metric.type,
                    "labels": dict(series.metric.labels),
                },
                "resource": {
                    "type": series.resource.type,
                    "labels": dict(series.resource.labels),
                },
                "metric_kind": monitoring_v3.MetricDescriptor.MetricKind(
                    series.metric_kind
                ).name,
                "value_type": monitoring_v3.MetricDescriptor.ValueType(
                    series.value_type
                ).name,
                "points": [],
            }

            for point in series.points:
                point_data = {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "value": {},
                }

                if point.value.HasField("double_value"):
                    point_data["value"] = {"double_value": point.value.double_value}
                elif point.value.HasField("int64_value"):
                    point_data["value"] = {"int64_value": point.value.int64_value}
                elif point.value.HasField("bool_value"):
                    point_data["value"] = {"bool_value": point.value.bool_value}
                elif point.value.HasField("string_value"):
                    point_data["value"] = {"string_value": point.value.string_value}

                series_data["points"].append(point_data)

            export_data["time_series"].append(series_data)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp_file:
            json.dump(export_data, tmp_file, indent=2, default=str)
            tmp_file_path = tmp_file.name

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"metrics/{metric_name}/{timestamp_str}/export.json"

        bucket = storage_client.bucket(bucket_name)

        try:
            bucket = storage_client.get_bucket(bucket_name)
        except:
            bucket = storage_client.create_bucket(bucket_name, location="US")

        blob = bucket.blob(blob_name)
        blob.upload_from_filename(tmp_file_path)

        os.unlink(tmp_file_path)

        archive_info = {
            "status": "success",
            "metric": metric_name,
            "window_hours": window_hours,
            "export_timestamp": export_data["export_timestamp"],
            "storage_location": {
                "bucket": bucket_name,
                "blob": blob_name,
                "uri": f"gs://{bucket_name}/{blob_name}",
            },
            "data_summary": {
                "series_count": len(export_data["time_series"]),
                "total_points": sum(
                    len(series["points"]) for series in export_data["time_series"]
                ),
            },
        }

        return archive_info

    except Exception as e:
        return {"status": "error", "metric": metric_name, "error": str(e)}


def create_metrics_snapshot_archive(
    metrics_list: List[str], window_hours: int = 24, bucket_name: str = None
) -> Dict[str, Any]:
    """Create an archive of multiple metric snapshots."""

    storage_client = storage.Client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not bucket_name:
        bucket_name = f"{project_id}-metrics-snapshots"

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_id = f"snapshot_{timestamp_str}"

    results = {
        "snapshot_id": snapshot_id,
        "timestamp": datetime.now().isoformat(),
        "project_id": project_id,
        "metrics": [],
        "storage_info": {
            "bucket": bucket_name,
            "base_path": f"snapshots/{snapshot_id}/",
        },
    }

    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        bucket = storage_client.create_bucket(bucket_name, location="US")

    for metric_name in metrics_list:
        export_result = export_metrics_to_storage(
            metric_name=metric_name, window_hours=window_hours, bucket_name=bucket_name
        )

        if export_result.get("status") == "success":
            metric_blob_name = f"snapshots/{snapshot_id}/{metric_name}/data.json"

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as tmp_file:
                json.dump(export_result, tmp_file, indent=2, default=str)
                tmp_file_path = tmp_file.name

            blob = bucket.blob(metric_blob_name)
            blob.upload_from_filename(tmp_file_path)

            os.unlink(tmp_file_path)

            results["metrics"].append(
                {
                    "name": metric_name,
                    "status": "archived",
                    "location": f"gs://{bucket_name}/{metric_blob_name}",
                }
            )
        else:
            results["metrics"].append(
                {
                    "name": metric_name,
                    "status": "failed",
                    "error": export_result.get("error", "Unknown error"),
                }
            )

    summary_blob_name = f"snapshots/{snapshot_id}/summary.json"
    summary_blob = bucket.blob(summary_blob_name)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp_file:
        json.dump(results, tmp_file, indent=2, default=str)
        tmp_file_path = tmp_file.name

    summary_blob.upload_from_filename(tmp_file_path)
    os.unlink(tmp_file_path)

    results["summary_location"] = f"gs://{bucket_name}/{summary_blob_name}"

    successful = sum(1 for m in results["metrics"] if m["status"] == "archived")
    results["summary"] = {
        "total_metrics": len(metrics_list),
        "successful": successful,
        "failed": len(metrics_list) - successful,
        "success_rate": (successful / len(metrics_list)) * 100 if metrics_list else 0,
    }

    return results


from datetime import timedelta
