import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def query_error_logs(log_name, severity, start_time, end_time):
    query_client = client.logging_query_client()
    filter_ = f"severity={severity} AND timestamp >= '{start_time}' AND timestamp <= '{end_time}'"
    entries = query_client.query(filter_=filter_, resource_names=[log_name])
    for entry in entries:
        print(entry)


if __name__ == "__main__":
    log_name = "my_log"
    severity = "ERROR"
    start_time = "2026-04-22T00:00:00Z"
    end_time = "2026-04-22T23:59:59Z"
    query_error_logs(log_name, severity, start_time, end_time)
