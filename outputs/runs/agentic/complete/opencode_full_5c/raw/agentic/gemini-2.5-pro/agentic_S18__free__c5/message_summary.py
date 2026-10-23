from google.cloud import logging_v2


def write_summary_log(log_name: str, processed_count: int, failed_count: int):
    """Writes a message processing summary to Google Cloud Logging."""
    client = logging_v2.LoggingServiceV2Client()

    log_entry = {
        "log_name": f"projects/{client.project}/logs/{log_name}",
        "resource": {"type": "global"},
        "json_payload": {
            "message": "Message processing summary",
            "processed_count": processed_count,
            "failed_count": failed_count,
        },
        "severity": "INFO",
    }

    client.write_log_entries(entries=[log_entry])
    print("Wrote summary log to Google Cloud Logging.")


if __name__ == "__main__":
    # This is an example, and will not be executed.
    LOG_NAME = "message_processing_summary"
    write_summary_log(LOG_NAME, 100, 5)
