from google.cloud import bigquery


def message_summary(payload, config=None):
    client = bigquery.Client()
    job = client.query(payload["query"])
    rows = list(job.result())
    return {"row_count": len(rows), "project": client.project, "has_rows": bool(rows)}
