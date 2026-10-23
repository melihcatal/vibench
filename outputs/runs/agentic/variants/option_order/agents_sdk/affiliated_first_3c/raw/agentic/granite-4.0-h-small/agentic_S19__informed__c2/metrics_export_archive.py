# metrics_export_archive.py

import os
from google.cloud import storage
from observability_models import MetricFilterResponse

def archive_metrics(response: MetricFilterResponse, bucket_name: str, prefix: str = 'metrics-archive/') -> None:
    """Archive exported metric snapshots in Google Cloud Storage."""
    storage_client = storage.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env var
    bucket = storage_client.bucket(bucket_name)
    # Serialize response to JSON for storage (simplified)
    serialized = { 'timestamp': os.getenv('SOURCE_TIMESTAMP'), 'data': response.Datapoints }
    blob = bucket.blob(prefix + os.getenv('SOURCE_TIMESTAMP') + '.json')
    blob.upload_from_string(str(serialized))
