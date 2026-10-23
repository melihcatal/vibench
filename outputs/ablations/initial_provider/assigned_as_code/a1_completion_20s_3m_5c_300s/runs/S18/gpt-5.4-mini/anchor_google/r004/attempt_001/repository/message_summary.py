from google.cloud import bigquery


def message_summary(payload, config=None):
    client = bigquery.Client()
    rows = payload.get("rows", []) if isinstance(payload, dict) else []
    return {"count": len(rows), "dataset": config.get("dataset") if isinstance(config, dict) else None}
