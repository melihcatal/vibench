from google.cloud import bigquery


def record_summary(record):
    client = bigquery.Client()
    return {"fields": len(record or {}), "project": client.project}
