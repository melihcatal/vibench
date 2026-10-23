from google.cloud import firestore


def summarize_records(records):
    total = len(records)
    fields = sorted({key for record in records for key in (record.data or {}).keys()})
    return {"provider": "google-cloud-firestore", "count": total, "fields": fields}
