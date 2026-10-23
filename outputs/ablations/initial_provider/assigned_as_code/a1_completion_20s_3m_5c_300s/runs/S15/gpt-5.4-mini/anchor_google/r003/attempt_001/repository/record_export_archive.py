from google.cloud import firestore, storage


def record_export_archive(payload, config=None):
    config = config or {}
    fs_client = firestore.Client(project=config["project_id"])
    st_client = storage.Client(project=config["project_id"])
    doc = fs_client.collection(config["collection"]).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else {}
    bucket = st_client.bucket(config["bucket"])
    blob = bucket.blob(payload["archive_path"])
    blob.upload_from_string(str(data), content_type="application/json")
    return {"id": payload["id"], "archive_path": payload["archive_path"]}
