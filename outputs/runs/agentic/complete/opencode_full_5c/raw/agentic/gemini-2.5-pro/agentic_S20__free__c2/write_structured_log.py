import json
from observability_client import get_logging_client
from observability_models import LOG_NAME


def write_log_entry():
    logging_client = get_logging_client()
    logger = logging_client.logger(LOG_NAME)

    log_payload = {
        "message": "User signed in successfully.",
        "user_id": "user12345",
        "ip_address": "192.168.1.100",
        "event_type": "user_login",
    }

    logger.log_struct(log_payload, severity="INFO")


if __name__ == "__main__":
    write_log_entry()
