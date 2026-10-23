from google.cloud import bigquery

from observability_client import build_bigquery_client, load_config, time_window


def fetch_recent_logs(field_name: str = "service", field_value: str = "api") -> list[dict]:
    config = load_config()
    client = build_bigquery_client()
    start, end = time_window(30)
    query = f'''
        SELECT *
        FROM `{config.project_id}.{config.dataset_id}.{config.table_id}`
        WHERE {field_name} = @field_value
          AND timestamp BETWEEN @start_time AND @end_time
        ORDER BY timestamp DESC
        LIMIT 100
    '''
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("field_value", "STRING", field_value),
            bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start),
            bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end),
        ]
    )
    rows = client.query(query, job_config=job_config).result()
    return [dict(row.items()) for row in rows]


if __name__ == "__main__":
    fetch_recent_logs()
