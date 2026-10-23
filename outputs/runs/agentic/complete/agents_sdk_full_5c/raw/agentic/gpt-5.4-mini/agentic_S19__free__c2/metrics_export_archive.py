from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Dict

from google.cloud import monitoring_v3

from observability_client import load_config, storage_client, metric_client
from observability_models import MetricsExportArchiveRequest


def metrics_export_archive(request: MetricsExportArchiveRequest) -> Dict[str, str]:
    config = load_config()
    client = metric_client()
    storage = storage_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)
    interval = monitoring_v3.TimeInterval({"end_time": end_time, "start_time": start_time})
    series = client.list_time_series(request={"name": f"projects/{config.project_id}", "filter": f'metric.type = "{request.metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    payload = []
    for ts in series:
        for point in ts.points:
            payload.append({"metric": dict(ts.metric.labels), "resource": dict(ts.resource.labels), "value": float(point.value.double_value or point.value.int64_value or point.value.distribution_value.count)})
    bucket = storage.bucket(config.bucket_name)
    blob_name = request.destination_blob_name or f"metric-archives/{request.metric_type.replace('/', '_')}-{end_time.strftime('%Y%m%dT%H%M%SZ')}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(payload), content_type="application/json")
    return {"bucket": config.bucket_name or "", "blob": blob_name, "status": "archived"}
