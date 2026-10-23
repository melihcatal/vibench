from google.cloud import bigquery


def rotation_summary(project_id: str, dataset: str, table: str):
    client = bigquery.Client(project=project_id)
    query = f"SELECT secret_id, MAX(rotated_at) AS last_rotated FROM `{project_id}.{dataset}.{table}` GROUP BY secret_id"
    return [dict(row) for row in client.query(query).result()]
