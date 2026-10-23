import google.cloud.logging
import json

client = google.cloud.logging.Client()
client.setup_logging()


def summarize_error_logs(log_name, severity, start_time, end_time):
    logger = client.logger(log_name)
    filter_ = (
        f'severity={severity} AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    )
    entries = logger.list_entries(filter_=filter_)
    summary = {"total_errors": 0, "error_messages": []}
    for entry in entries:
        summary["total_errors"] += 1
        summary["error_messages"].append(entry.payload)
    return json.dumps(summary, indent=2)


if __name__ == "__main__":
    print(
        summarize_error_logs(
            "my_log", "ERROR", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"
        )
    )
