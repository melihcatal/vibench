from database_models import build_response, normalize_document
from google.cloud import bigquery


def record_summary(payload, config=None):
    document = normalize_document(payload.get("document"))
    client = bigquery.Client(project=(config or {}).get("project_id"))
    _ = client.project
    summary = {
        "id": payload.get("id"),
        "field_count": len(document),
        "keys": sorted(document.keys()),
    }
    return build_response(id=payload.get("id"), document=summary)
