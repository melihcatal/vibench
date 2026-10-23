from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.protobuf import timestamp_pb2
import datetime

def query_error_logs(project_id: str, severity: str, time_range_seconds: int):
    client = logging_v2.LoggingServiceV2Client()

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(seconds=time_range_seconds)

    # Convert datetime objects to protobuf Timestamp
    start_timestamp_proto = timestamp_pb2.Timestamp()
    start_timestamp_proto.FromDatetime(start_time)

    end_timestamp_proto = timestamp_pb2.Timestamp()
    end_timestamp_proto.FromDatetime(now)

    # Build the filter string
    filter_string = f'severity>={severity} AND timestamp>="{start_time.isoformat()}"'

    # The project resource name
    project_name = f"projects/{project_id}"

    print(f"Querying logs for project: {project_id} with severity: {severity} and time range: {time_range_seconds} seconds ago.")
    print(f"Filter: {filter_string}")

    try:
        response = client.list_log_entries(
            resource_names=[project_name],
            filter=filter_string,
            order_by=log_entry_pb2.LogEntry.Timestamp.Name,
        )

        found_logs = False
        for entry in response:
            found_logs = True
            print(f"Log Entry:")
            print(f"  Timestamp: {entry.timestamp.ToDatetime()}")
            print(f"  Severity: {entry.severity}")
            print(f"  Resource: {entry.resource.type}")
            print(f"  Log Name: {entry.log_name}")
            if entry.text_payload:
                print(f"  Payload: {entry.text_payload}")
            elif entry.json_payload:
                print(f"  Payload: {dict(entry.json_payload)}")
            elif entry.proto_payload:
                print(f"  Payload: {entry.proto_payload}")
            print("-" * 20)

        if not found_logs:
            print("No error logs found matching the criteria.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'your-gcp-project-id' with your actual GCP Project ID
    # Ensure you have authenticated to GCP (e.g., using `gcloud auth application-default login`)
    # For example:
    # project_id = "your-gcp-project-id"
    # severity = "ERROR" # Options: DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
    # time_range_seconds = 3600 # Last 1 hour

    print("Please set your GCP project ID, desired severity, and time range in the script.")
    print("Example usage (uncomment and replace placeholders):")
    # project_id = "your-gcp-project-id"
    # severity = "ERROR"
    # time_range_seconds = 3600
    # query_error_logs(project_id, severity, time_range_seconds)

    # Placeholder for demonstration if actual project_id is not set
    # In a real scenario, this would be uncommented and configured by the user.
    # For testing purposes, we can call it with dummy values, but it will fail without proper auth.
    print("\nNote: This script requires GCP authentication and a valid project ID to run successfully.")
    print("Please ensure 'google-cloud-logging' is installed (`pip install google-cloud-logging`).")
