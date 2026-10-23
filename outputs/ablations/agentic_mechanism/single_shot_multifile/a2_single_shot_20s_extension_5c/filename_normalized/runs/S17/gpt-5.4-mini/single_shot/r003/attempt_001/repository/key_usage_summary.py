from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import bigquery

from security_client import load_security_config


def key_usage_summary(days: int = 30) -> List[Dict[str, Any]]:
    config = load_security_config()
    client = bigquery.Client(project=config.project_id)
    query = f"""
        SELECT
          resource.labels.key_ring_name AS key_ring,
          resource.labels.crypto_key_name AS crypto_key,
          COUNT(*) AS event_count,
          MIN(timestamp) AS first_seen,
          MAX(timestamp) AS last_seen
        FROM `{config.project_id}.cloudaudit_googleapis_com_activity_*`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
          AND protoPayload.serviceName = 'cloudkms.googleapis.com'
        GROUP BY key_ring, crypto_key
        ORDER BY event_count DESC
    """
    job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)])
    rows = client.query(query, job_config=job_config).result()
    return [dict(row) for row in rows]
