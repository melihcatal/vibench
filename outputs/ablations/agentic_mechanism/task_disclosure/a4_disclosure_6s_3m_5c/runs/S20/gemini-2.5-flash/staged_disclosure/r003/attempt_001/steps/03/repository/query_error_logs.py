from google.cloud import logging_v2
import datetime

def query_error_logs(project_id, severity="ERROR", time_range_minutes=60):
    """
    Queries recent error log entries from Google Cloud Logging.

    Args:
        project_id (str): Your Google Cloud project ID.
        severity (str): The minimum severity level to filter by (e.g., "ERROR", "WARNING", "INFO").
                        Defaults to "ERROR".
        time_range_minutes (int): The time range in minutes to look back for logs.
                                  Defaults to 60 minutes.
    """
    # [START logging_v2_client_initialization]
    # Google Cloud Logging client
    client = logging_v2.LoggingServiceV2Client()
    # [END logging_v2_client_initialization]

    # Calculate the timestamp for filtering
    now = datetime.datetime.utcnow()
    past_time = now - datetime.timedelta(minutes=time_range_minutes)
    timestamp_filter = f'timestamp >= "{past_time.isoformat("T")}Z"'

    # Construct the filter string
    # identifiable provider-specific log filter syntax
    filter_string = f'resource.type="global" AND severity>="{severity}" AND {timestamp_filter}'

    # The full resource name of the parent resource, in this case, a project.
    parent = f"projects/{project_id}"

    print(f"Querying logs for project: {project_id} with filter: {filter_string}")

    try:
        # [START logging_v2_list_log_entries]
        for entry in client.list_log_entries(request={"parent": parent, "filter": filter_string}):
            print(f"Log Entry: {entry.json_payload if entry.json_payload else entry.text_payload if entry.text_payload else entry.proto_payload if entry.proto_payload else entry.log_name}")
        # [END logging_v2_list_log_entries]
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # For example: "your-gcp-project-id"
    # Ensure you have authenticated to Google Cloud and have the necessary permissions.
    # e.g., using `gcloud auth application-default login`
    YOUR_PROJECT_ID = "your-gcp-project-id" 

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
        print("You can set it as an environment variable or directly in the script.")
    else:
        query_error_logs(YOUR_PROJECT_ID, severity="WARNING", time_range_minutes=120)
