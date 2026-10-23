# metrics_export_archive.py
# Archive exported metric snapshots in managed object storage

from observability_client import ObservabilityClient
from observability_models import MetricResponse
import os
import json
import tempfile
import shutil

STORAGE_SERVICE = "google"  # example: adjust to your preferred provider

def archive_exported_metric(service: str, metric_response: MetricResponse, bucket: str = "metrics-export", prefix: str = "snapshots") -> str:
    """Persist a MetricResponse to object storage and return its path identifier.", service, MetricResponse

    The function serializes the response to JSON and uploads it to the chosen object-storage bucket.",
    client = ObservabilityClient.get_client(service)
    # Determine storage client based on STORAGE_SERVICE setting
    if STORAGE_SERVICE == "google":
        # Google Cloud Storage SDK
        from google.cloud import storage
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        client_lib = storage.Client()
        bucket_obj = client_lib.bucket(bucket)
        # Create a deterministic filename from metric name and timestamp range
        start, end = metric_response.metadata.get("start_time", ""), metric_response.metadata.get("end_time", "")
        filename = f"{prefix}/{metric_response.metric}_{start.replace('T','_')[:10]}_{end.replace('T','_')[:10]}.json"
    elif STORAGE_SERVICE == "aws":
        # Amazon S3 SDK
        import boto3
        client_lib = boto3.client("s3", region_name="us-east-1")
        filename = f"{prefix}/{metric_response.metric}_{metric_response.metadata.get('start_time','')}.json"
    elif STORAGE_SERVICE == "azure":
        # Azure Blob Storage SDK
        from azure.storage.blob import BlobServiceClient
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service.get_container_client(bucket)
        filename = f"{prefix}/{metric_response.metric}_{metric_response.metadata.get('start_time','')}.json"
    elif STORAGE_SERVICE == "alibaba":
        # Alibaba Cloud OSS SDK
        from oss2 import Auth, Bucket
        auth = Auth(os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
        bucket_obj = Bucket(auth, f"http://{bucket}.oss-cn-hangzhou.aliyuncs.com", bucket)
        filename = f"{prefix}/{metric_response.metric}_{metric_response.metadata.get('start_time','')}.json"
    else:
        raise ValueError(f"Unsupported storage service {STORAGE_SERVICE} for archiving")

    # Serialize payload
    payload = {
        "service": metric_response.service,
        "metric": metric_response.metric,
        "datapoints": metric_response.datapoints,
        "metadata": metric_response.metadata
    }
    # Use temporary file to upload (simplifies multi‑provider SDK usage)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        json.dump(payload, tmp)
        tmp_path = tmp.name
    # Upload to bucket/prefix
    if STORAGE_SERVICE == "google":
        blob = bucket_obj.blob(filename)
        blob.upload_from_filename(tmp_path)
    elif STORAGE_SERVICE == "aws":
        client_lib.upload_file(tmp_path, bucket, filename)
    elif STORAGE_SERVICE == "azure":
        blob_client = bucket_obj.get_blob_client(container=bucket, blob=filename)
        with open(tmp_path, "rb") as data:
            blob_client.upload_blob(data)
    elif STORAGE_SERVICE == "alibaba":
        bucket_obj.put_object_from_file(filename, tmp_path)
    else:
        raise ValueError(f"Unsupported storage service {STORAGE_SERVICE} during upload")

    shutil.unlink(tmp_path)  # clean up temp file
    # Return a path identifier (depends on provider)
    return f"{bucket}/{filename}"
