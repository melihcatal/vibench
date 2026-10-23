import os
import json
import tempfile
from typing import Dict, List, Any, Optional, BinaryIO
from datetime import datetime
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
from google.cloud.storage import Blob


class MetricsExporter:
    def __init__(
        self, bucket_name: Optional[str] = None, credentials_path: Optional[str] = None
    ):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.bucket_name = bucket_name or os.getenv("GCS_METRICS_BUCKET")
        if not self.bucket_name:
            raise ValueError("GCS_METRICS_BUCKET environment variable must be set")

        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def export_metrics_to_gcs(
        self, metrics_data: Dict[str, Any], export_name: str, file_format: str = "json"
    ) -> Dict[str, Any]:
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            blob_name = f"metrics_exports/{export_name}_{timestamp}.{file_format}"

            if file_format == "json":
                content = json.dumps(metrics_data, indent=2, default=str)
                content_type = "application/json"
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(content, content_type=content_type)

            return {
                "export_name": export_name,
                "blob_name": blob_name,
                "bucket": self.bucket_name,
                "file_format": file_format,
                "size_bytes": len(content),
                "url": f"gs://{self.bucket_name}/{blob_name}",
                "timestamp": timestamp,
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error exporting metrics to GCS: {e}")
            raise

    def archive_metric_snapshot(
        self,
        snapshot_data: Dict[str, Any],
        snapshot_name: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        try:
            timestamp = datetime.utcnow().isoformat()
            blob_name = f"metric_snapshots/{snapshot_name}/{timestamp}/snapshot.json"

            archive_data = {
                "snapshot_name": snapshot_name,
                "timestamp": timestamp,
                "data": snapshot_data,
                "metadata": metadata or {},
            }

            content = json.dumps(archive_data, indent=2, default=str)

            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(content, content_type="application/json")

            if metadata:
                blob.metadata = metadata
                blob.patch()

            return {
                "snapshot_name": snapshot_name,
                "blob_name": blob_name,
                "bucket": self.bucket_name,
                "size_bytes": len(content),
                "url": f"gs://{self.bucket_name}/{blob_name}",
                "timestamp": timestamp,
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error archiving metric snapshot: {e}")
            raise

    def export_metrics_as_csv(
        self, metrics_data: List[Dict[str, Any]], export_name: str
    ) -> Dict[str, Any]:
        try:
            if not metrics_data:
                raise ValueError("No metrics data to export")

            import csv
            import io

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            blob_name = f"metrics_exports/{export_name}_{timestamp}.csv"

            output = io.StringIO()
            writer = csv.writer(output)

            headers = set()
            for item in metrics_data:
                headers.update(item.keys())
            headers = sorted(headers)

            writer.writerow(headers)

            for item in metrics_data:
                row = [item.get(header, "") for header in headers]
                writer.writerow(row)

            content = output.getvalue()

            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(content, content_type="text/csv")

            return {
                "export_name": export_name,
                "blob_name": blob_name,
                "bucket": self.bucket_name,
                "file_format": "csv",
                "size_bytes": len(content),
                "url": f"gs://{self.bucket_name}/{blob_name}",
                "timestamp": timestamp,
                "row_count": len(metrics_data),
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error exporting metrics as CSV: {e}")
            raise

    def create_compressed_archive(
        self, metrics_data: Dict[str, Any], archive_name: str
    ) -> Dict[str, Any]:
        try:
            import zipfile
            import io

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            blob_name = f"metric_archives/{archive_name}_{timestamp}.zip"

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for key, data in metrics_data.items():
                    if isinstance(data, (dict, list)):
                        content = json.dumps(data, indent=2, default=str)
                        zip_file.writestr(f"{key}.json", content)
                    else:
                        zip_file.writestr(f"{key}.txt", str(data))

                zip_file.writestr(
                    "manifest.json",
                    json.dumps(
                        {
                            "archive_name": archive_name,
                            "timestamp": timestamp,
                            "files": list(metrics_data.keys()),
                            "file_count": len(metrics_data),
                        },
                        indent=2,
                    ),
                )

            zip_content = zip_buffer.getvalue()

            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(zip_content, content_type="application/zip")

            return {
                "archive_name": archive_name,
                "blob_name": blob_name,
                "bucket": self.bucket_name,
                "file_format": "zip",
                "size_bytes": len(zip_content),
                "url": f"gs://{self.bucket_name}/{blob_name}",
                "timestamp": timestamp,
                "file_count": len(metrics_data),
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error creating compressed archive: {e}")
            raise

    def list_metric_exports(
        self, prefix: str = "metrics_exports/"
    ) -> List[Dict[str, Any]]:
        try:
            blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix)

            exports = []
            for blob in blobs:
                exports.append(
                    {
                        "name": blob.name,
                        "size": blob.size,
                        "updated": blob.updated,
                        "url": f"gs://{self.bucket_name}/{blob.name}",
                    }
                )

            return exports

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error listing metric exports: {e}")
            raise

    def delete_old_exports(self, days_old: int = 30) -> Dict[str, Any]:
        try:
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days_old)

            blobs = self.storage_client.list_blobs(
                self.bucket_name, prefix="metrics_exports/"
            )

            deleted_count = 0
            deleted_files = []

            for blob in blobs:
                if blob.updated.replace(tzinfo=None) < cutoff_date:
                    blob.delete()
                    deleted_count += 1
                    deleted_files.append(blob.name)

            return {
                "deleted_count": deleted_count,
                "deleted_files": deleted_files,
                "cutoff_date": cutoff_date.isoformat(),
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error deleting old exports: {e}")
            raise

    def generate_signed_url(
        self, blob_name: str, expiration_hours: int = 24
    ) -> Dict[str, Any]:
        try:
            blob = self.bucket.blob(blob_name)

            if not blob.exists():
                raise ValueError(f"Blob {blob_name} does not exist")

            url = blob.generate_signed_url(
                expiration=expiration_hours * 3600, method="GET"
            )

            return {
                "blob_name": blob_name,
                "signed_url": url,
                "expiration_hours": expiration_hours,
                "expires_at": (
                    datetime.utcnow() + timedelta(hours=expiration_hours)
                ).isoformat(),
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Storage API error: {e}")
            raise
        except Exception as e:
            print(f"Error generating signed URL: {e}")
            raise


def export_metrics_data(
    metrics_data: Dict[str, Any], export_name: str
) -> Dict[str, Any]:
    exporter = MetricsExporter()
    return exporter.export_metrics_to_gcs(metrics_data, export_name)


def archive_daily_metrics_snapshot(snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
    exporter = MetricsExporter()

    date_str = datetime.utcnow().strftime("%Y%m%d")
    snapshot_name = f"daily_snapshot_{date_str}"

    metadata = {
        "snapshot_type": "daily",
        "date": date_str,
        "source": "google_cloud_monitoring",
    }

    return exporter.archive_metric_snapshot(snapshot_data, snapshot_name, metadata)


def export_metrics_report(
    metrics_report: Dict[str, Any], report_name: str
) -> Dict[str, Any]:
    exporter = MetricsExporter()

    archive_data = {
        "report": metrics_report,
        "summary": {
            "generated_at": datetime.utcnow().isoformat(),
            "report_name": report_name,
            "sections": list(metrics_report.keys()),
        },
    }

    return exporter.create_compressed_archive(archive_data, report_name)


def backup_metric_configurations(
    configs: List[Dict[str, Any]], backup_name: str
) -> Dict[str, Any]:
    exporter = MetricsExporter()

    backup_data = {
        "configurations": configs,
        "backup_info": {
            "name": backup_name,
            "timestamp": datetime.utcnow().isoformat(),
            "config_count": len(configs),
        },
    }

    return exporter.export_metrics_to_gcs(backup_data, f"config_backup_{backup_name}")


def export_metric_alerts(
    alerts: List[Dict[str, Any]], export_name: str
) -> Dict[str, Any]:
    exporter = MetricsExporter()

    export_data = {
        "alerts": alerts,
        "export_info": {
            "name": export_name,
            "timestamp": datetime.utcnow().isoformat(),
            "alert_count": len(alerts),
        },
    }

    return exporter.export_metrics_as_csv(
        [alert for alert in alerts if isinstance(alert, dict)], f"alerts_{export_name}"
    )
