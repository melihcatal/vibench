# LATER-STEP
import os
from google.cloud import storage
from observability_client import get_monitoring_client
from observability_models import MetricRequest

def metrics_export_archive(request: MetricRequest, bucket_name: str = 'my-metrics-archive'):
    """Archive exported metric snapshots in managed object storage.

    Fetches metric points for the given request and uploads a JSON file to Cloud Storage.
    """
    client = get_monitoring_client()
    # Simple query similar to query_metric_window (could be expanded)
    response = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{request.metric_name}"',
            startTime=request.start_time,
            endTime=request.end_time,
            pageSize=request.limit
        )
        .execute()
    points = []
    for series in response.get('timeSeries', []):
        for pt in series.get('points', []):
            points.append({'interval': pt.get('interval'), 'value': pt.get('value')})
    # Serialize to JSON string
    import json, datetime
    archive_entry = {
        'metric_name': request.metric_name,
        'start_time': request.start_time,
        'end_time': request.end_time,
        'points': points,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    json_blob = json.dumps(archive_entry, indent=2).encode('utf-8')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    file_name = f"metrics_{request.metric_name}_{request.start_time.replace(':', '_')}_to_{request.end_time.replace(':', '_')}.json"
    blob = bucket.blob(file_name)
    blob.upload_from_string(json_blob)
    return f"Archived {file_name} to bucket {bucket_name}"
