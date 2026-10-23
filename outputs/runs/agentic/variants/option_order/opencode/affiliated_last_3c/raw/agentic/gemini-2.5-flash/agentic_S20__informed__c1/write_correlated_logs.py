import os
from observability_client import get_logging_client
from observability_models import CorrelatedLogEntry


def write_correlated_logs(entry: CorrelatedLogEntry):
    client = get_logging_client()
    logger = client.logger(entry.log_name)

    # Google Cloud Logging allows batching log entries
    # The 'trace' field can be used for correlation, or a custom label/jsonPayload field
    for log_data in entry.entries:
        # Assuming each log_data dict contains 'message', 'severity', and potentially 'jsonPayload'
        # and a 'correlation_id' within jsonPayload or as a label
        logger.log(
            log_data.get("message"),
            severity=log_data.get("severity", "INFO"),
            resource={
                "type": entry.resource_type,
                "labels": entry.resource_labels,
            },
            labels=log_data.get("labels"),
            json_payload=log_data.get("json_payload"),
        )
    print(f"Correlated logs written to {entry.log_name}")


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        correlation_id = "req-abc-123"
        correlated_entry = CorrelatedLogEntry(
            log_name="my-application-log",
            resource_type="global",
            resource_labels={
                "project_id": project_id,
            },
            entries=[
                {
                    "message": "Request started.",
                    "severity": "INFO",
                    "json_payload": {"correlation_id": correlation_id, "step": 1},
                },
                {
                    "message": "Processing data.",
                    "severity": "INFO",
                    "json_payload": {
                        "correlation_id": correlation_id,
                        "step": 2,
                        "data_size": 1024,
                    },
                },
                {
                    "message": "Request completed.",
                    "severity": "INFO",
                    "json_payload": {"correlation_id": correlation_id, "step": 3},
                },
            ],
        )
        write_correlated_logs(correlated_entry)
