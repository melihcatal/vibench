from google.cloud import bigquery


def message_summary(payload, config=None):
    config = config or {}
    counts = payload.get("counts", {})
    total = sum(int(value) for value in counts.values())
    client = bigquery.Client(project=config.get("project_id"))
    return {
        "provider": "google_bigquery",
        "project_id": client.project,
        "total_messages": total,
        "counts": counts,
        "successful": int(counts.get("success", 0)),
        "failed": int(counts.get("failed", 0)),
    }
