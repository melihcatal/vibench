from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter, ArrayQueryParameter
from datetime import datetime, timedelta
from typing import List, Dict, Any

from identity_client import GCP_PROJECT_ID
from identity_models import AuditSummaryReport

def summarize_federated_login_events(
    dataset_id: str,
    table_id: str,
    start_time: datetime,
    end_time: datetime,
) -> AuditSummaryReport:
    """
    Summarizes federated login audit events stored in Google BigQuery.
    """
    client = bigquery.Client(project=GCP_PROJECT_ID)
    table_ref = f"{GCP_PROJECT_ID}.{dataset_id}.{table_id}"

    # Basic query to count total, successful, failed logins and unique users
    query = f"""
    SELECT
        COUNT(*) as total_logins,
        COUNTIF(login_successful = TRUE) as successful_logins,
        COUNTIF(login_successful = FALSE) as failed_logins,
        COUNT(DISTINCT user_id) as unique_users,
        ARRAY_AGG(STRUCT(provider, provider_count) ORDER BY provider_count DESC LIMIT 5) as top_providers
    FROM (
        SELECT
            provider,
            user_id,
            login_successful,
            COUNT(*) OVER (PARTITION BY provider) as provider_count
        FROM `{table_ref}`
        WHERE timestamp BETWEEN @start_time AND @end_time
    )
    GROUP BY provider
    """
    # Note: The query for `top_providers` needs adjustment. A subquery is more appropriate.
    # Let's revise for better aggregation.

    query = f"""
    SELECT
        COUNT(*) as total_logins,
        COUNTIF(login_successful = TRUE) as successful_logins,
        COUNTIF(login_successful = FALSE) as failed_logins,
        COUNT(DISTINCT user_id) as unique_users,
        ARRAY(
            SELECT AS STRUCT provider, COUNT(*) AS count
            FROM `{table_ref}`
            WHERE timestamp BETWEEN @start_time AND @end_time
            GROUP BY provider
            ORDER BY count DESC
            LIMIT 5
        ) AS top_providers
    FROM `{table_ref}`
    WHERE timestamp BETWEEN @start_time AND @end_time
    """


    job_config = QueryJobConfig(
        query_parameters=[
            ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
            ScalarQueryParameter("end_time", "TIMESTAMP", end_time),
        ]
    )

    print(f"Executing BigQuery audit summary for {table_ref}...")
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    summary_data: Dict[str, Any] = next(iter(results))._as_dict() # Get the first row as a dictionary

    report_id = f"audit-summary-{start_time.strftime('%Y%m%d%H%M%S')}-{end_time.strftime('%Y%m%d%H%M%S')}"

    summary_report = AuditSummaryReport(
        report_id=report_id,
        start_date=start_time,
        end_date=end_time,
        total_logins=summary_data.get("total_logins", 0),
        successful_logins=summary_data.get("successful_logins", 0),
        failed_logins=summary_data.get("failed_logins", 0),
        unique_users=summary_data.get("unique_users", 0),
        top_providers=summary_data.get("top_providers", []),
        top_regions=[], # Geolocation of IPs not included in this basic query, can be added.
        summary_notes="Summarized federated login events from BigQuery."
    )
    print("Successfully generated audit summary report.")
    return summary_report

if __name__ == "__main__":
    # Example Usage
    # Replace with your actual BigQuery dataset and table IDs
    GCP_DATASET_ID = "federated_identity_audit"
    GCP_AUDIT_TABLE_ID = "login_events"

    # Ensure you have a BigQuery table named 'login_events' in 'federated_identity_audit'
    # with a schema similar to FederatedLoginEvent.to_dict()
    # For example, columns like: event_id, timestamp, provider, user_id, login_successful, etc.

    end_dt = datetime.utcnow()
    start_dt = end_dt - timedelta(days=7) # Last 7 days

    print(f"Attempting to summarize events from {start_dt} to {end_dt}")

    try:
        report = summarize_federated_login_events(GCP_DATASET_ID, GCP_AUDIT_TABLE_ID, start_dt, end_dt)
        print("\n--- Audit Summary Report ---")
        print(report.to_dict())
    except Exception as e:
        print(f"Error generating audit summary: {e}")
        print("Please ensure your GCP_PROJECT_ID, BigQuery dataset, and table exist and are correctly configured.")
        print("Also, ensure you have appropriate IAM permissions to access BigQuery.")
