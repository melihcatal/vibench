import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def query_error_logs(log_name, severity, start_time, end_time):
    logger = client.logger(log_name)
    filter_ = (
        f'severity={severity} AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    )
    entries = logger.list_entries(filter_=filter_)
    for entry in entries:
        print(entry.payload)


if __name__ == "__main__":
    query_error_logs("my_log", "ERROR", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z")
