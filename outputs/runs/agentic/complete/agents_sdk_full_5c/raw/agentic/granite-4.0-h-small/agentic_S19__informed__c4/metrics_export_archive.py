# [LATER-STEP] metrics_export_archive.py
# Archive exported metric snapshots in managed object storage using Google Cloud Storage SDK

import os
import io
from google.cloud import storage
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import TimeInterval
from datetime import datetime

storage_client = storage.Client()
bucket_name = os.getenv("ARCHIVE_BUCKET", "metrics-archive")
bucket = storage_client.bucket(bucket_name)

def metrics_export_archive(metric_type: str, window_minutes: int = 60, **labels) -> str:
    """Export recent metric points to CSV and store them in Cloud Storage.

    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **labels: Dimension filters for the query.

    Returns:
        Public URI of the uploaded CSV file.
    """
    end_ts = int(datetime.now().timestamp())
    start_ts = end_ts - 60 * window_minutes
    interval = TimeInterval.from_seconds(start_ts, end_ts)
    request = {
        "name": get_monitoring_client().project_path(),
        "metric_type": metric_type,
        "interval": interval,
        "filter_": f"labels.{next(iter(labels))}='{labels[next(iter(labels))]}"
        if labels else ""
    }
    # Collect points (simulated; real implementation would call list_time_series)
    points = []
    for ts in get_monitoring_client().list_time_series(request):
        points.extend(ts.points)
    # Build CSV content
    lines = ["timestamp,value"]
    for p in points:
        lines.append(f"{p.interval.start}:{p.value}")
    csv_data = io.StringIO("\n".join(lines))
    # Upload to Cloud Storage
    blob_name = f"{metric_type.replace('/', '_')}_archive_{end_ts}.csv"
    blob = bucket.blob(blob_name)
    blob.upload_from_file(csv_data, content_type="text/csv")
    return f"gs://{bucket_name}/{blob_name}"
