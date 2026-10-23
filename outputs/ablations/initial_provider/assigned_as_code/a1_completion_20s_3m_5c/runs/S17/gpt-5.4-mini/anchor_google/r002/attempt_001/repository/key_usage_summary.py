from google.cloud import bigquery


def key_usage_summary(payload, config=None):
    config = config or {}
    client = bigquery.Client()
    query = payload["query"]
    job = client.query(query, project=config.get("project_id"))
    rows = [dict(row) for row in job]
    return {"rows": rows}
