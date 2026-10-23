import os
import datetime
from google.cloud import storage
from observability_client import MonitoringClient
from observability_models import MetricQueryRequest

def metrics_export_archive(metric_query: MetricQueryRequest, bucket_name: str = 'my-metrics-archive'):
    """Archive exported metric snapshots in managed object storage (Google Cloud Storage).

    Requires env var: GOOGLE_APPLICATION_CREDENTIALS
    """
    # ----- GCS client ----- 
    gcs = storage.Client()
    bucket = gcs.bucket(bucket_name)
    if not bucket.exists():
        bucket.create()  # creates bucket if it does not exist

    # ----- Get metric data ----- 
    query_dict = metric_query.to_dict()
    client = MonitoringClient()
    raw = client.fetch_time_series(query_dict)
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    object_name = f'metrics_snapshot_{metric_query.metric}_{timestamp}.json'
    blob = bucket.blob(object_name)
    blob.upload_from_string(payload=str(raw), content_type='application/json')

    return {'status': 'archived', 'bucket': bucket_name, 'object_name': object_name}
