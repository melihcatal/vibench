import os
from observability_client import get_logging_client
from observability_models import CorrelatedLog


def write_correlated_log_events(log_name: str, correlated_logs: list[CorrelatedLog]):
    """Writes multiple correlated log events to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(log_name)

    entries = []
    for log_event in correlated_logs:
        entries.append(
            logger.entry_from_json(
                json_data=log_event.to_json(), severity=log_event.severity
            )
        )
    logger.write(entries)
    print(f"{len(correlated_logs)} correlated log entries written to {log_name}.")


if __name__ == "__main__":
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # GOOGLE_CLOUD_PROJECT is a provider-identifying signal
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        log_name = "my-correlated-request-log"
        correlation_id = "req-abc-123"
        logs = [
            CorrelatedLog(
                message="Request received", correlation_id=correlation_id, step="start"
            ),
            CorrelatedLog(
                message="Processing data",
                correlation_id=correlation_id,
                step="process",
                severity="DEBUG",
            ),
            CorrelatedLog(
                message="Response sent",
                correlation_id=correlation_id,
                step="end",
                severity="INFO",
            ),
        ]
        write_correlated_log_events(log_name, logs)
