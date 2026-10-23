import os
import json
from datetime import datetime, timedelta
from google.cloud import bigquery


def summarize_message_processing(start_time=None, end_time=None, project_id=None):
    """Summarize message processing results using BigQuery."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if start_time is None:
        start_time = datetime.utcnow() - timedelta(hours=24)
    if end_time is None:
        end_time = datetime.utcnow()

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the query to summarize message processing
    # Assuming we have a BigQuery table with message processing records
    dataset_id = os.environ.get("BIGQUERY_DATASET", "messaging_analytics")
    table_id = os.environ.get("BIGQUERY_MESSAGES_TABLE", "message_processing")

    query = f"""
    SELECT
        COUNT(*) as total_messages,
        COUNTIF(success = true) as successful_messages,
        COUNTIF(success = false) as failed_messages,
        COUNTIF(dead_letter_info IS NOT NULL) as dead_letter_messages,
        AVG(processing_time_ms) as avg_processing_time_ms,
        MIN(processing_time_ms) as min_processing_time_ms,
        MAX(processing_time_ms) as max_processing_time_ms,
        APPROX_QUANTILES(processing_time_ms, 4)[OFFSET(2)] as median_processing_time_ms,
        COUNT(DISTINCT message_type) as distinct_message_types,
        TIMESTAMP_TRUNC(publish_time, HOUR) as processing_hour
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE publish_time BETWEEN TIMESTAMP('{start_time.isoformat()}') 
        AND TIMESTAMP('{end_time.isoformat()}')
    GROUP BY processing_hour
    ORDER BY processing_hour DESC
    LIMIT 24
    """

    try:
        # Execute the query
        query_job = client.query(query)
        results = query_job.result()

        summary_data = []
        for row in results:
            summary_data.append(
                {
                    "processing_hour": row.processing_hour.isoformat(),
                    "total_messages": row.total_messages,
                    "successful_messages": row.successful_messages,
                    "failed_messages": row.failed_messages,
                    "dead_letter_messages": row.dead_letter_messages,
                    "success_rate": (row.successful_messages / row.total_messages * 100)
                    if row.total_messages > 0
                    else 0,
                    "avg_processing_time_ms": row.avg_processing_time_ms,
                    "min_processing_time_ms": row.min_processing_time_ms,
                    "max_processing_time_ms": row.max_processing_time_ms,
                    "median_processing_time_ms": row.median_processing_time_ms,
                    "distinct_message_types": row.distinct_message_types,
                }
            )

        # Calculate overall summary
        if summary_data:
            total_messages = sum(row["total_messages"] for row in summary_data)
            total_successful = sum(row["successful_messages"] for row in summary_data)
            total_failed = sum(row["failed_messages"] for row in summary_data)
            total_dead_letter = sum(row["dead_letter_messages"] for row in summary_data)

            overall_summary = {
                "time_period": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                },
                "totals": {
                    "total_messages": total_messages,
                    "successful_messages": total_successful,
                    "failed_messages": total_failed,
                    "dead_letter_messages": total_dead_letter,
                    "success_rate": (total_successful / total_messages * 100)
                    if total_messages > 0
                    else 0,
                    "failure_rate": (total_failed / total_messages * 100)
                    if total_messages > 0
                    else 0,
                    "dead_letter_rate": (total_dead_letter / total_messages * 100)
                    if total_messages > 0
                    else 0,
                },
                "hourly_breakdown": summary_data,
                "data_source": f"bigquery://{project_id}/{dataset_id}/{table_id}",
            }
        else:
            overall_summary = {
                "time_period": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                },
                "totals": {
                    "total_messages": 0,
                    "successful_messages": 0,
                    "failed_messages": 0,
                    "dead_letter_messages": 0,
                    "success_rate": 0,
                    "failure_rate": 0,
                    "dead_letter_rate": 0,
                },
                "hourly_breakdown": [],
                "data_source": f"bigquery://{project_id}/{dataset_id}/{table_id}",
                "note": "No data found for the specified time period",
            }

        return overall_summary

    except Exception as e:
        return {
            "error": str(e),
            "query": query,
            "project_id": project_id,
            "dataset": dataset_id,
            "table": table_id,
        }


def store_processing_record(record, project_id=None):
    """Store a single processing record in BigQuery."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    client = bigquery.Client(project=project_id)

    dataset_id = os.environ.get("BIGQUERY_DATASET", "messaging_analytics")
    table_id = os.environ.get("BIGQUERY_MESSAGES_TABLE", "message_processing")

    table_ref = client.dataset(dataset_id).table(table_id)

    # Prepare the row
    row = {
        "message_id": record.get("message_id", ""),
        "success": record.get("success", False),
        "processing_time_ms": record.get("processing_time_ms", 0),
        "publish_time": record.get("publish_time", datetime.utcnow().isoformat()),
        "message_type": record.get("message_type", "unknown"),
        "source": record.get("source", "unknown"),
        "error": record.get("error"),
        "dead_letter_info": json.dumps(record.get("dead_letter_info"))
        if record.get("dead_letter_info")
        else None,
        "processing_timestamp": datetime.utcnow().isoformat(),
    }

    errors = client.insert_rows_json(table_ref, [row])

    if errors:
        return {"success": False, "errors": errors}
    else:
        return {"success": True, "record": row}


if __name__ == "__main__":
    # Example usage
    summary = summarize_message_processing()
    print(f"Message processing summary: {json.dumps(summary, indent=2)}")
