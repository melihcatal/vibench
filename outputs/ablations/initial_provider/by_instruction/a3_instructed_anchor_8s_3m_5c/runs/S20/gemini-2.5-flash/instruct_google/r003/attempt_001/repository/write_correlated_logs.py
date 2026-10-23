from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry

def write_correlated_logs(log_name: str, entry: CorrelatedLogEntry):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    # Google Cloud Logging allows custom fields in json_payload
    # We'll include correlation_id in the json_payload for structured logging
    payload = {
        "message": entry.message,
        "correlation_id": entry.correlation_id,
        **entry.json_payload
    }

    logger.log(
        json_payload=payload,
        severity=entry.severity
    )

if __name__ == "__main__":
    # Example Usage:
    correlation_id = "req-12345"
    
    log_entry_1 = CorrelatedLogEntry(
        message="User initiated checkout process.",
        correlation_id=correlation_id,
        severity="INFO",
        json_payload={
            "user_id": "user-abc",
            "step": "start_checkout"
        }
    )
    write_correlated_logs("my-application-requests", log_entry_1)

    log_entry_2 = CorrelatedLogEntry(
        message="Payment gateway response received.",
        correlation_id=correlation_id,
        severity="INFO",
        json_payload={
            "user_id": "user-abc",
            "payment_status": "success"
        }
    )
    write_correlated_logs("my-application-requests", log_entry_2)
