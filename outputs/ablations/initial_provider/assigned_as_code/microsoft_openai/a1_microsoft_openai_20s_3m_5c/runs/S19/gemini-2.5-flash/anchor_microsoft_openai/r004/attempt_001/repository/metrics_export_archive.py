from observability_client import GcpObservabilityClient
from google.cloud import storage
from datetime import datetime

def metrics_export_archive(payload, config=None):
    config = config or {}
    bucket_name = config['gcs_bucket_name']
    file_content = payload['snapshot_data']
    # Generate a filename, e.g., metrics_snapshot_2023-10-27T10-00-00Z.json
    timestamp = datetime.utcnow().isoformat(timespec='seconds').replace(':', '-') + 'Z'
    file_name = f"metrics_snapshot_{payload.get('metric_name', 'generic')}_{timestamp}.json"
    content_type = payload.get('content_type', 'application/json')

    client = GcpObservabilityClient().storage_client

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Upload the file content
    blob.upload_from_string(file_content, content_type=content_type)

    return {
        'bucket': bucket_name,
        'file_name': file_name,
        'public_url': blob.public_url
    }
