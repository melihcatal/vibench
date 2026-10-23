from google.cloud import monitoring_v3
from google.cloud import storage
from observability_client import get_monitoring_client
from datetime import datetime, timedelta
import json
import tempfile

def export_metrics_to_gcs(project_id: str, metric_type: str, bucket_name: str, hours: int = 1) -> str:
    monitoring_client = get_monitoring_client()
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    query_request = {
        "name": f"projects/{project_id}",
        "filter": f'metric.type="{metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        }
    }
    
    data_points = []
    for series in monitoring_client.list_time_series(request=query_request):
        for point in series.points:
            data_points.append({
                "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                "value": point.value.double_value,
                "resource_labels": dict(series.resource.labels)
            })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        json.dump(data_points, tmp_file)
        tmp_file_path = tmp_file.name
    
    blob_name = f"metrics_export/{metric_type}_{int(datetime.utcnow().timestamp())}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(tmp_file_path)
    
    return f"gs://{bucket_name}/{blob_name}"