from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.protobuf import timestamp_pb2
import datetime

def summarize_error_logs(project_id: str, filter_string: str, time_range_seconds: int = 3600):
    """
    Summarizes error log findings for incident review from Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        filter_string: A filter string for log entries (e.g., 'resource.type="kubernetes_container" AND severity>=ERROR').
        time_range_seconds: The time range in seconds to look back for logs (default: 1 hour).

    Returns:
        A string summarizing the error logs, or an empty string if no errors are found.
    """
    client = logging_v2.LoggingServiceV2Client()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(seconds=time_range_seconds)

    # Convert datetime objects to protobuf Timestamp
    timestamp_proto_start = timestamp_pb2.Timestamp()
    timestamp_proto_start.FromDatetime(start_time)
    timestamp_proto_end = timestamp_pb2.Timestamp()
    timestamp_proto_end.FromDatetime(now)

    full_filter = f'{filter_string} AND timestamp>="{timestamp_proto_start.isoformat()}Z" AND timestamp<="{timestamp_proto_end.isoformat()}Z"'

    # Fetch log entries
    response = client.list_log_entries(
        resource_names=[project_name],
        filter=full_filter,
        order_by="timestamp desc",
        page_size=100
    )

    summary_messages = []
    error_count = 0
    unique_errors = set()

    for entry in response.iterate_all():
        error_count += 1
        if entry.text_payload:
            unique_errors.add(entry.text_payload)
            summary_messages.append(f"  - {entry.timestamp.ToDatetime().isoformat()}: {entry.text_payload[:200]}...")
        elif entry.json_payload:
            payload_str = str(entry.json_payload)
            unique_errors.add(payload_str)
            summary_messages.append(f"  - {entry.timestamp.ToDatetime().isoformat()}: {payload_str[:200]}...")
        else:
            # Fallback for other payload types, just include the severity and timestamp
            summary_messages.append(f"  - {entry.timestamp.ToDatetime().isoformat()}: {entry.severity} log entry.")


    if error_count > 0:
        summary = f"Incident Summary for Project: {project_id}
"
        summary += f"Time Range: Last {time_range_seconds} seconds
"
        summary += f"Total error entries found: {error_count}
"
        summary += f"Unique error messages (first 200 chars): {len(unique_errors)}

"
        summary += "Recent Error Log Entries:
"
        summary += "\n".join(summary_messages)
        return summary
    else:
        return f"No error logs found for project {project_id} within the last {time_range_seconds} seconds matching filter: '{filter_string}'."

