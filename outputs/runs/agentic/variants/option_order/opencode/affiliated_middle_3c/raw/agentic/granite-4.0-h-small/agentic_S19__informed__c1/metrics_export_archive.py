# [LATER-STEP] metrics_export_archive.py

import os
from .observability_client import get_azure_client, get_gcp_client
from .observability_models import MetricQueryRequest, MetricResponse

# Choose storage provider: Azure Blob Storage (default) or Google Cloud Storage
# Requires AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_KEY for Azure
# Requires GOOGLE_APPLICATION_CREDENTIALS for GCP

STORAGE_SERVICE = os.getenv('METRICS_EXPORT_STORAGE', 'azure')

if STORAGE_SERVICE == 'azure':
    from azure.storage.blob import BlobServiceClient, BlobClient
    blob_service = BlobServiceClient(
        account_url=os.getenv('AZURE_STORAGE_ACCOUNT_URL'),
        credential=os.getenv('AZURE_STORAGE_KEY')
    )
elif STORAGE_SERVICE == 'gcp':
    from google.cloud import storage
    client_gcp = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
else:
    raise ValueError("Unsupported storage service configured")

ARCHIVE_BUCKET = os.getenv('METRICS_ARCHIVE_BUCKET', 'metrics-exports')

ARCHIVE_PATH = 'exported_snapshots/'


def archive_snapshot(service, metric_request: MetricQueryRequest, snapshot_bytes: bytes):
    """Archive a metric snapshot (e.g., exported JSON/CSV) to managed object storage.",
    # Generate a unique filename based on request and timestamp
    import datetime
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    filename = f"{ARCHIVE_PATH}{service}_{metric_request.metric_name}_{ts}.json"
    if STORAGE_SERVICE == 'azure':
        blob_client = blob_service.get_blob_client(container=ARCHIVE_BUCKET, blob=filename)
        blob_client.upload_blob(snapshot_bytes, overwrite=True)
        print(f"Archived to Azure Blob: {filename}")
    elif STORAGE_SERVICE == 'gcp':
        bucket = client_gcp.get_bucket(ARCHIVE_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(snapshot_bytes)
        print(f"Archived to GCP Cloud Storage: {filename}")
    else:
        raise RuntimeError("Unexpected storage service")

# Example usage (for local testing)
if __name__ == '__main__':
    sample_request = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).timestamp() * 1000),
        end_time=int(datetime.datetime.utcnow().timestamp() * 1000),
        granularity_ms=60 * 1000,
        dimensions={'InstanceId': 'i-test'}
    )
    dummy_snapshot = b"[{'timestamp':1609459200000, 'value':75}]"
    archive_snapshot('cloudwatch', sample_request, dummy_snapshot)
