from google.cloud import firestore
from google.cloud import storage

from database_client import load_config


def record_export_archive(payload, config=None):
    config = load_config(config)
    firestore_client = firestore.Client(project=config["project_id"])
    storage_client = storage.Client(project=config["project_id"])
    snapshot = firestore_client.collection(config["collection"]).document(payload["id"]).get()
    bucket = storage_client.bucket(config["bucket"])
    blob = bucket.blob(payload["archive_path"])
    blob.upload_from_string(str(snapshot.to_dict() or {}), content_type="application/json")
    return {"id": payload["id"], "archive_path": payload["archive_path"]}
