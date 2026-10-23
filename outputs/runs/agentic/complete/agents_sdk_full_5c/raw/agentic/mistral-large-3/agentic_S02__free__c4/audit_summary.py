from datetime import datetime, timedelta
from google.cloud import bigquery
from identity_models import LoginAuditRecord

def summarize_login_audits(time_range_hours: int = 24) -> dict:
    client = bigquery.Client()
    query = f"""
        SELECT
            provider,
            status,
            COUNT(*) as count
        FROM
            `federated_login.audit_logs`
        WHERE
            timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {time_range_hours} HOUR)
        GROUP BY
            provider, status
    """
    query_job = client.query(query)
    results = query_job.result()

    summary = {}
    for row in results:
        provider = row['provider']
        status = row['status']
        if provider not in summary:
            summary[provider] = {}
        summary[provider][status] = row['count']

    return summary