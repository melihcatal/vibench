import uuid
from observability_client import get_gcp_logger
from observability_models import CorrelatedLog


def write_correlated_logs(log_name: str, logs: list[CorrelatedLog]):
    """
    Writes a series of correlated logs to Google Cloud Logging.

    Args:
        log_name: The name of the log.
        logs: A list of CorrelatedLog objects.
    """
    logger = get_gcp_logger(log_name)

    for log_entry in logs:
        logger.log_struct(log_entry.to_dict(), severity=log_entry.severity)
    print(f"Wrote {len(logs)} correlated logs to {log_name}")


if __name__ == "__main__":
    # Example Usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID environment variables

    correlation_id = str(uuid.uuid4())

    log_batch = [
        CorrelatedLog(
            message="Initiating transaction.",
            correlation_id=correlation_id,
            service_name="service-A",
            severity="INFO",
        ),
        CorrelatedLog(
            message="Contacting downstream service.",
            correlation_id=correlation_id,
            service_name="service-A",
            severity="DEBUG",
        ),
        CorrelatedLog(
            message="Transaction successful.",
            correlation_id=correlation_id,
            service_name="service-B",
            severity="INFO",
        ),
    ]

    write_correlated_logs("correlated-app-log", log_batch)
