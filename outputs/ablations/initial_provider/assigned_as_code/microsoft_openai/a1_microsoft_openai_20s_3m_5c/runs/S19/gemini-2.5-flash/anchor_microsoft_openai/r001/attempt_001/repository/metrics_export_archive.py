import os
from google.cloud import storage
import json

def archive_metrics_export(payload):
    bucket_name = payload.get('bucket_name')
    destination_blob_name = payload.get('destination_blob_name')
    metrics_data = payload.get('metrics_data')

    if not bucket_name or not destination_blob_name or not metrics_data:
        return {'error': 'Missing bucket_name, destination_blob_name, or metrics_data in payload'}

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the metrics data as a JSON file
    blob.upload_from_string(json.dumps(metrics_data), content_type='application/json')

    return {'message': f'Metrics data archived to gs://{bucket_name}/{destination_blob_name}'}
