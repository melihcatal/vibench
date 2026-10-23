import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def write_log(log_name, log_data):
    logger = client.logger(log_name)
    logger.log_struct(log_data)


if __name__ == "__main__":
    write_log("my_log", {"event": "test_event", "severity": "INFO"})
