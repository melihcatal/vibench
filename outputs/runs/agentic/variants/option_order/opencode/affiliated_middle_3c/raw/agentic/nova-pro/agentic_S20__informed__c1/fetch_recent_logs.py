import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def fetch_recent_logs(log_name, field, value, start_time, end_time):
    logger = client.logger(log_name)
    filter_ = (
        f'{field}="{value}" AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    )
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)


if __name__ == "__main__":
    fetch_recent_logs(
        "my_log", "event", "test_event", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"
    )
