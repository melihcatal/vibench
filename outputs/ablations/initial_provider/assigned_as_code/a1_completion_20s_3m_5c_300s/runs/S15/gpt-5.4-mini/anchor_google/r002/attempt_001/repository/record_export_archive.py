from google.cloud import firestore, storage

from database_client import load_config
from database_models import normalize_document


def record_export_archive(payload, config=None):
    config = load_config(config)
    db_client = firestore.Client(project=config["project_id"])
    st_client = storage.Client(project=config["project_id"])
    snapshot = db_client.collection(config["collection"]).document(payload["id"]).get()
    document = normalize_document(snapshot) or {}
    bucket = st_client.bucket(config["bucket"])
    blob = bucket.blob(payload.get("name") or f"{payload['id']}.json")
    blob.upload_from_string(str(document), content_type="application/json")
    return {"id": payload["id"], "archive_uri": f"gs://{bucket.name}/{blob.name}"}
