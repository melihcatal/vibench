import json

from observability_client import get_storage_client

def metrics_export_archive(payload, config=None):
    config = config or {}
    client = get_storage_client()

    bucket_name = payload["bucket_name"]
    destination_blob_name = payload["destination_blob_name"]
    metric_data = payload["metric_data"]

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # The metric_data is assumed to be a dictionary that needs to be serialized to JSON
    blob.upload_from_string(json.dumps(metric_data), content_type="application/json")

    return {"bucket_name": bucket_name, "destination_blob_name": destination_blob_name, "status": "success"}
