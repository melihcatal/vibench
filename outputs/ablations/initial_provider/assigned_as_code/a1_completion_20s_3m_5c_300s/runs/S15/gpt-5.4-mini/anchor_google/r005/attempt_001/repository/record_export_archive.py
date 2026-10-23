from google.cloud import storage


def record_export_archive(payload, config=None):
    config = config or {}
    client = storage.Client(project=config["project_id"])
    bucket = client.bucket(config["bucket"])
    blob = bucket.blob(payload["archive_path"])
    blob.upload_from_string(payload["content"])
    return {"archive_path": payload["archive_path"]}
