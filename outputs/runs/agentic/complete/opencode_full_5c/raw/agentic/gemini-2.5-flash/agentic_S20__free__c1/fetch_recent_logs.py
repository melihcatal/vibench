import os
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

def fetch_recent_logs(field_name: str, field_value: str, time_range_minutes: int = 30) -> list[LogQueryResult]:
    client = ObservabilityClient(project_id=PROJECT_ID)

    now = datetime.utcnow()
    time_ago = now - timedelta(minutes=time_range_minutes)

    # Constructing a filter for a specific field value
    # This assumes the field is either a top-level field or within jsonPayload
    # For jsonPayload fields, the syntax is jsonPayload.fieldName="value"
    filter_str = (
        f"("{field_name}"=\"{field_value}\" OR jsonPayload.{field_name}=\"{field_value}\") AND "
        f"timestamp>=\"{time_ago.isoformat('T')[:-3]}Z\" AND "
        f"timestamp<=\"{now.isoformat('T')[:-3]}Z\""
    )

    print(f"Fetching recent logs for {field_name}=\"{field_value}\" in the last {time_range_minutes} minutes...")
    results = client.query_logs(filter_str=filter_str)

    if results:
        print(f"Found {len(results)} logs:")
        for res in results:
            print(f"  [{res.timestamp}] [{res.severity}] {res.message} (Trace: {res.trace or 'N/A'})")
    else:
        print("No recent logs found matching the criteria.")
    return results

if __name__ == "__main__":
    # Example usage:
    # To test this, you might need to write a log first with a specific `requestId` in its jsonPayload
    # from write_correlated_logs import write_correlated_logs
    # correlation_id = str(uuid.uuid4())
    # write_correlated_logs(request_id=correlation_id, user_id="test-user-123", transaction_amount=99.99)
    # import time; time.sleep(5) # Give logging a moment to ingest

    # Example: fetch logs by a specific request ID
    # Replace 'your-request-id' with an actual request ID from your logs
    recent_logs = fetch_recent_logs(field_name="requestId", field_value="your-request-id-example", time_range_minutes=10)
