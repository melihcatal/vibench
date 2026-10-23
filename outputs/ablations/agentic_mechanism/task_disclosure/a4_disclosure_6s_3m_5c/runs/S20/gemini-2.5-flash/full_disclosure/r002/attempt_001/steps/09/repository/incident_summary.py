from google.cloud import logging

def summarize_error_logs(project_id: str, time_range: str = "24h") -> str:
    """
    Summarizes error-log findings for incident review.

    Args:
        project_id: The Google Cloud project ID.
        time_range: The time range for logs (e.g., "1h", "24h", "7d").

    Returns:
        A summary string of the error logs.
    """
    client = logging.Client(project=project_id)
    logger = client.logger("incident-review-logger")

    # Define a filter for error logs within the specified time range
    # A more sophisticated time range handling would be needed for production
    # This example assumes 'time_range' can be directly incorporated or converted.
    # For a real implementation, 'time_range' would be converted into a timestamp
    # filter for Google Cloud Logging.
    filter_string = f'severity >= ERROR timestamp >= "{time_range_to_timestamp(time_range)}"'

    entries = client.list_entries(
        filter_=filter_string,
        order_by=logging.DESCENDING,
        page_size=100  # Limit the number of entries for summarization
    )

    error_messages = {}
    for entry in entries:
        if entry.payload:
            message = str(entry.payload)
            error_messages[message] = error_messages.get(message, 0) + 1

    if not error_messages:
        return "No error logs found for the specified time range."

    summary = f"Incident Summary for Project: {project_id} (Last {time_range}):\n"
    for message, count in error_messages.items():
        summary += f"- Found '{message}' {count} time(s).\n"

    return summary

def time_range_to_timestamp(time_range_str: str) -> str:
    """
    Converts a human-readable time range string to a timestamp string for logging queries.
    This is a simplified placeholder and would require a more robust implementation
    for production use, likely using datetime and timedelta.
    """
    import datetime
    now = datetime.datetime.utcnow()
    if time_range_str.endswith("h"):
        hours = int(time_range_str[:-1])
        delta = datetime.timedelta(hours=hours)
    elif time_range_str.endswith("d"):
        days = int(time_range_str[:-1])
        delta = datetime.timedelta(days=days)
    else: # Default to 24 hours if format is not recognized
        delta = datetime.timedelta(hours=24)
    
    start_time = now - delta
    return start_time.isoformat("T") + "Z" # Google Cloud Logging expects 'Z' for UTC
