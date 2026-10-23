import os
from typing import List, Dict
from datetime import datetime, timedelta
from google.cloud import bigquery
from messaging_models import ProcessedMessage


def summarize_message_processing(
    start_time: datetime = None, end_time: datetime = None
) -> Dict:
    """Summarize message processing results using Google BigQuery."""
    if start_time is None:
        start_time = datetime.utcnow() - timedelta(hours=24)
    if end_time is None:
        end_time = datetime.utcnow()

    client = bigquery.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    )

    dataset_id = os.environ.get("BIGQUERY_DATASET", "message_processing")
    table_id = os.environ.get("BIGQUERY_TABLE", "processed_messages")

    query = f"""
    SELECT 
        COUNT(*) as total_messages,
        SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successful_messages,
        SUM(CASE WHEN success = false THEN 1 ELSE 0 END) as failed_messages,
        AVG(processing_time_ms) as avg_processing_time_ms,
        MIN(processing_time_ms) as min_processing_time_ms,
        MAX(processing_time_ms) as max_processing_time_ms,
        COUNT(DISTINCT JSON_EXTRACT_SCALAR(event_message, '$.event_type')) as distinct_event_types
    FROM `{dataset_id}.{table_id}`
    WHERE TIMESTAMP(processed_at) BETWEEN TIMESTAMP('{start_time.isoformat()}') 
        AND TIMESTAMP('{end_time.isoformat()}')
    """

    query_job = client.query(query)
    results = list(query_job.result())

    if results:
        row = results[0]
        summary = {
            "total_messages": row.total_messages,
            "successful_messages": row.successful_messages,
            "failed_messages": row.failed_messages,
            "success_rate": (row.successful_messages / row.total_messages * 100)
            if row.total_messages > 0
            else 0,
            "avg_processing_time_ms": row.avg_processing_time_ms,
            "min_processing_time_ms": row.min_processing_time_ms,
            "max_processing_time_ms": row.max_processing_time_ms,
            "distinct_event_types": row.distinct_event_types,
            "time_period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
        }
    else:
        summary = {
            "total_messages": 0,
            "successful_messages": 0,
            "failed_messages": 0,
            "success_rate": 0,
            "avg_processing_time_ms": 0,
            "min_processing_time_ms": 0,
            "max_processing_time_ms": 0,
            "distinct_event_types": 0,
            "time_period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
        }

    print(f"Message processing summary: {summary}")
    return summary


def store_processed_message(processed_message: ProcessedMessage):
    """Store processed message record in BigQuery."""
    client = bigquery.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    )

    dataset_id = os.environ.get("BIGQUERY_DATASET", "message_processing")
    table_id = os.environ.get("BIGQUERY_TABLE", "processed_messages")

    table_ref = client.dataset(dataset_id).table(table_id)

    row = processed_message.to_dict()

    errors = client.insert_rows_json(table_ref, [row])

    if errors:
        print(f"Errors inserting row: {errors}")
    else:
        print(f"Stored processed message {processed_message.message_id}")


if __name__ == "__main__":
    summary = summarize_message_processing()
    print(f"Summary: {summary}")
