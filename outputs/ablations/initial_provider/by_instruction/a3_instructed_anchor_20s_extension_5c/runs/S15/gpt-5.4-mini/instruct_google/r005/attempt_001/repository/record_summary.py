from database_models import normalize_document


def record_summary(record):
    data = normalize_document(record)
    return {"provider": "google_firestore", "summary": {k: data.get(k) for k in list(data)[:5]}}
