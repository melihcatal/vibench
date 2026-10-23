import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def write_correlated_logs(log_name, log_data, correlation_id):
    logger = client.logger(log_name)
    log_data["correlation_id"] = correlation_id
    logger.log_struct(log_data)


if __name__ == "__main__":
    log_name = "my_log"
    log_data = {"event": "user_login", "user_id": "12345"}
    correlation_id = "abcdef123456"
    write_correlated_logs(log_name, log_data, correlation_id)
