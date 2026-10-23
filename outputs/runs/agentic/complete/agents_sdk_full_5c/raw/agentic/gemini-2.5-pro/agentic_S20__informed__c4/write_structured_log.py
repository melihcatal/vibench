import json
from observability_client import get_logging_client
from observability_models import StructuredLog

LOG_NAME = "my-structured-log"


def write_structured_log_event(log_entry: StructuredLog):
    """
    Writes a single structured log entry to Google Cloud Logging.

    Args:
        log_entry (StructuredLog): The structured log entry to write.
    """
    logging_client = get_logging_client()
    logger = logging_client.logger(LOG_NAME)

    payload = log_entry.model_dump(exclude_none=True)

    logger.log_json(
        json_payload=payload,
        severity=log_entry.severity,
    )
    print(f"Wrote structured log to {LOG_NAME}: {json.dumps(payload)}")


# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     example_log = StructuredLog(
#         message="User successfully logged in.",
#         severity="INFO",
#         service_name="auth-service",
#         correlation_id="abc-123-xyz-789",
#         additional_data={"user_id": "user1234"}
#     )
#     write_structured_log_event(example_log)
