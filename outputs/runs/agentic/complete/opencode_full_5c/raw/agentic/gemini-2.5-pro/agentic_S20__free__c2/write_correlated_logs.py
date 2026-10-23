import uuid
from observability_client import get_logging_client
from observability_models import LOG_NAME


def write_correlated_log_entries():
    logging_client = get_logging_client()
    logger = logging_client.logger(LOG_NAME)
    correlation_id = str(uuid.uuid4())

    log_payload_1 = {
        "message": "Processing started for request.",
        "correlation_id": correlation_id,
        "stage": "begin_processing",
    }
    logger.log_struct(log_payload_1, severity="INFO")

    log_payload_2 = {
        "message": "Fetching user data from database.",
        "correlation_id": correlation_id,
        "stage": "data_retrieval",
    }
    logger.log_struct(log_payload_2, severity="DEBUG")

    log_payload_3 = {
        "message": "Processing finished for request.",
        "correlation_id": correlation_id,
        "stage": "end_processing",
    }
    logger.log_struct(log_payload_3, severity="INFO")


if __name__ == "__main__":
    write_correlated_log_entries()
