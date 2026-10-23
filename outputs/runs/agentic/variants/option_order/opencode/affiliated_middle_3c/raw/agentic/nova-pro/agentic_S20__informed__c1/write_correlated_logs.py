import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def write_correlated_logs(log_name, correlation_id, log_data):
    logger = client.logger(log_name)
    log_data["correlation_id"] = correlation_id
    logger.log_struct(log_data)


if __name__ == "__main__":
    write_correlated_logs(
        "my_log", "12345", {"event": "test_event", "severity": "INFO"}
    )
