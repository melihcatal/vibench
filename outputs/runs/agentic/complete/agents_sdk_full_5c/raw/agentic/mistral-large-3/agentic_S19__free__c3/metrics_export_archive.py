import os
from datetime import datetime
from google.cloud import storage
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client


def archive_metrics_export(metric_type: str, bucket_name: str, hours: int = 24) -> str:
    client = get_monitoring_client()
    storage_client = storage.Client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    query = (
        f'fetch gcp_metric :: {metric_type} '
        f'| within {hours}h'
    )
    
    result = client.query_time_series(
        name=f"projects/{project_id}",
        query=query
    )
    
    export_data = []
    for series in result.time_series:
        for point in series.points:
            export_data.append({
                "timestamp": point.interval.end_time.timestamp(),
                "value": point.value.double_value,
                "resource_labels": dict(series.resource.labels),
                "metric_labels": dict(series.metric.labels)
            })
    
    export_json = json.dumps(export_data, indent=2)
    filename = f"metrics_export_{metric_type}_{int(end_time.timestamp())}.json"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(export_json)
    
    return f"gs://{bucket_name}/{filename}"