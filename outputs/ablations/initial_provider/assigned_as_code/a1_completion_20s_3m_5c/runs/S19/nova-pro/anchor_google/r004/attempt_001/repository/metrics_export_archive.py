import os
import json

from google.cloud import storage

def metrics_export_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.get_bucket(config['bucket_name'])
    blob = bucket.blob(f"metrics/{payload['metric']}/{payload['timestamp']}.json")
    blob.upload_from_string(json.dumps(payload['data']), content_type='application/json')
    return {"status": "success"}
