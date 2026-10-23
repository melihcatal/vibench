from google.cloud import aiplatform


def record_summary(record: dict) -> dict:
    text = str(record)
    return {"summary": text[:280], "provider": "google_vertex_ai"}
