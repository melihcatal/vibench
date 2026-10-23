from google.cloud import storage

from observability_client import load_config, storage_client


def metrics_export_archive(blob_name: str, destination_blob_name: str) -> str:
    config = load_config()
    client = storage_client()
    bucket = client.bucket(config.bucket_name)
    source = bucket.blob(blob_name)
    destination = bucket.blob(destination_blob_name)
    destination.rewrite(source)
    return f"gs://{config.bucket_name}/{destination_blob_name}"
