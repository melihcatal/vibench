import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def write_log(log_name, log_data):
    logger = client.logger(log_name)
    logger.log_struct(log_data)


if __name__ == "__main__":
    log_name = "my_log"
    log_data = {"event": "user_login", "user_id": "12345"}
    write_log(log_name, log_data)
