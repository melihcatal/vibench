# [LATER-STEP] metrics_export_archive.py

import os
import json
import boto3
from datetime import datetime, timedelta
from observability_client import get_azure_monitor_client
from observability_models import MetricQueryRequest

# AWS credentials are handled by DefaultAWS credential chain (env vars, instance metadata, etc.)
s3_client = boto3.client('s3')
S3_BUCKET = os.getenv('METRICS_EXPORT_BUCKET')

ARCHIVE_PREFIX = 'azure-monitor-exports/'

ARCHIVE_FILE_SIZE_LIMIT = 10 * 1024 * 1024  # 10 MB per file

MAX_RETRIES = 3

def archive_metric_snapshot(metric_name: str, start_time: str, end_time: str, resource_id: str = None,
                            aggregation: str = 'Average') -> None:
    """Export a recent metric snapshot to an archived JSON file in S3.
    The function queries the metric over the provided window, bundles the points, and writes them
    to an S3 object under the configured bucket/prefix.
    Args:
        metric_name: Name of the Azure metric (e.g., 'CpuPercentage').
        start_time: ISO 8601 start timestamp (UTC).
        end_time: ISO 8601 end timestamp (UTC).
        resource_id: Azure resource ID (optional) for scoping.
        aggregation: Aggregation method (e.g., 'Average').
    """
    client = get_azure_monitor_client()
    request = MetricQueryRequest(metric=metric_name, start_time=start_time, end_time=end_time,
                                 aggregation=aggregation, interval='PT1M', resource_id=resource_id)
    response = client.query.get(resource_id, [request])
    points = response[0].flat_points if hasattr(response[0], 'flat_points') else []
    if not points:
        raise ValueError('No metric data to archive')
    payload = {
        'metric': metric_name,
        'time_window': {'start': start_time, 'end': end_time},
        'points': [{'timestamp': pt.timestamp.isoformat(), 'value': pt.value} for pt in points]
    }
    # Write to S3 in chunks respecting size limit
    json_str = json.dumps(payload, indent=2)
    if len(json_str.encode('utf-8')) > ARCHIVE_FILE_SIZE_LIMIT:
        # Split into multiple files based on time chunks
        split_interval = 'PT5M'  # 5‑minute slices
        start = datetime.fromisoformat(start_time[:-1])  # strip trailing Z
        end = datetime.fromisoformat(end_time[:-1])
        cur_start = start
        while cur_start < end:
            cur_end = min(cur_start + timedelta(minutes=5), end)
            sub_payload = {
                'metric': metric_name,
                'time_window': {'start': cur_start.isoformat() + 'Z', 'end': cur_end.isoformat() + 'Z'},
                'points': []
            }
            for pt in points:
                ts = pt.timestamp
                if cur_start <= ts <= cur_end:
                    sub_payload['points'].append({'timestamp': ts.isoformat() + 'Z', 'value': pt.value})
            _upload_to_s3(json.dumps(sub_payload, indent=2))
            cur_start = cur_end
    else:
        _upload_to_s3(json_str)


def _upload_to_s3(body: str):
    obj_key = f"{ARCHIVE_PREFIX}{datetime.utcnow().strftime('%Y/%m/%d/')}{datetime.utcnow().isoformat()}Z.json"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            s3_client.put_object(Bucket=S3_BUCKET, Key=obj_key, Body=body.encode('utf-8'))
            return
        except Exception as exc:
            retries += 1
            if retries >= MAX_RETRIES:
                raise RuntimeError(f"Failed to upload metrics after {MAX_RETRIES} attempts: {exc}")