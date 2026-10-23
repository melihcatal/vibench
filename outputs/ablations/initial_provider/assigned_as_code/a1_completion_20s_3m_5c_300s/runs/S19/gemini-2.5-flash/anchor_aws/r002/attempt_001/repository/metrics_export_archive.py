from typing import Dict, Any
import json

from observability_client import get_gcs_client

def metrics_export_archive(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    client = get_gcs_client()

    bucket_name = config["gcs_bucket_name"]
    destination_blob_name = payload["destination_blob_name"]
    data_to_archive = payload["data_to_archive"]

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Assuming data_to_archive is a dictionary or similar that can be serialized to JSON
    blob.upload_from_string(json.dumps(data_to_archive), content_type="application/json")

    return {"archive_status": f"Successfully archived data to gs://{bucket_name}/{destination_blob_name}"}
