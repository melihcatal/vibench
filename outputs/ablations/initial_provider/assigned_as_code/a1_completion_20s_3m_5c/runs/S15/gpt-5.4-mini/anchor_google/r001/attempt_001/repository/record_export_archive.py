from google.cloud import storage
from database_models import build_response, normalize_document


def record_export_archive(payload, config=None):
    config = config or {}
    document = normalize_document(payload.get("document"))
    client = storage.Client(project=config.get("project_id"))
    bucket = client.bucket(config["bucket"])
    blob = bucket.blob(f"{payload.get('id')}.json")
    blob.upload_from_string(str(document), content_type="application/json")
    return build_response(id=payload.get("id"), archived=True)
