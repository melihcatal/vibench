from datetime import datetime, timezone

from google.cloud import bigquery

from observability_client import build_bigquery_client, load_config, time_window


def query_error_logs() -> list[dict]:
    config = load_config()
    client = build_bigquery_client()
    start, end = time_window(60)
    query = f'''
        SELECT *
        FROM `{config.project_id}.{config.dataset_id}.{config.table_id}`
        WHERE severity IN ('ERROR', 'CRITICAL', 'ALERT', 'EMERGENCY')
          AND timestamp BETWEEN @start_time AND @end_time
        ORDER BY timestamp DESC
        LIMIT 50
    '''
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start),
            bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end),
        ]
    )
    rows = client.query(query, job_config=job_config).result()
    return [dict(row.items()) for row in rows]


if __name__ == "__main__":
    query_error_logs()
