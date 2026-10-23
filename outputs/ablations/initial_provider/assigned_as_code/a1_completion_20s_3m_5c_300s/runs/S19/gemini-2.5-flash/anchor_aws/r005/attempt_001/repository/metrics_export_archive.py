from google.cloud import storage
import json

def archive_metrics_export(payload, project_id):
    client = storage.Client(project=project_id)
    bucket_name = payload["bucket_name"]
    destination_blob_name = payload["destination_blob_name"]
    metrics_data = payload["metrics_data"]

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the metrics data as a JSON string
    blob.upload_from_string(json.dumps(metrics_data), content_type="application/json")

    return {
        "message": f"Metrics data archived successfully to gs://{bucket_name}/{destination_blob_name}",
        "bucket_name": bucket_name,
        "destination_blob_name": destination_blob_name,
        "self_link": blob.self_link
    }
