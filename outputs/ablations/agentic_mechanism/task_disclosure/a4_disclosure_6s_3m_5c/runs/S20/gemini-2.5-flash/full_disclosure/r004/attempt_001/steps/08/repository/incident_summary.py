from google.cloud import logging_v2
import datetime

def summarize_error_logs(project_id: str, time_range_hours: int = 24) -> str:
    """
    Summarizes error log findings for incident review from Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        time_range_hours: The number of hours to look back for error logs.

    Returns:
        A string summarizing the error logs.
    """
    client = logging_v2.Client(project=project_id)

    now = datetime.datetime.utcnow()
    past = now - datetime.timedelta(hours=time_range_hours)

    filter_string = (
        f'severity >= "ERROR" AND '
        f'timestamp >= "{past.isoformat(timespec="seconds")}Z" AND '
        f'timestamp < "{now.isoformat(timespec="seconds")}Z"'
    )

    entries = client.list_entries(
        filter_=filter_string,
        order_by=logging_v2.DESCENDING,
    )

    summary_messages = []
    error_counts = {}

    for entry in entries:
        log_name = entry.log_name.split("/")[-1]
        summary_messages.append(f"[{entry.timestamp}] {log_name}: {entry.payload}")
        error_counts[log_name] = error_counts.get(log_name, 0) + 1

    if not summary_messages:
        return f"No error logs found in the last {time_range_hours} hours for project {project_id}."

    summary_header = f"Incident Summary: Error Logs in Project {project_id} (Last {time_range_hours} hours)
"
    summary_counts = "Error Counts by Log Name:
" + "\n".join([f"- {name}: {count}" for name, count in error_counts.items()])
    
    return f"{summary_header}\n{summary_counts}\n\nRecent Error Log Entries (limited display):\n" + "\n".join(summary_messages[:10]) # Limit to 10 for brevity
