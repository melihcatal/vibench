from google.cloud import firestore

from database_client import load_config
from database_models import normalize_document


def record_translate(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    snapshot = client.collection(config["collection"]).document(payload["id"]).get()
    document = normalize_document(snapshot) or {}
    translated = dict(document)
    for field in payload.get("fields", ["title", "summary"]):
        if field in translated and translated[field] is not None:
            translated[field] = f"{translated[field]} ({payload.get('target_language', 'translated')})"
    return translated
