from observability_client import get_logging_client
import datetime


def write_correlated_logs(log_name: str, correlation_id: str, events: list[dict]):
    client = get_logging_client()
    logger = client.logger(log_name)

    for event in events:
        log_entry = {
            "correlation_id": correlation_id,
            "message": event.get("message"),
            "severity": event.get("severity", "INFO"),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            **{k: v for k, v in event.items() if k not in ["message", "severity"]},
        }
        logger.log_struct(log_entry)
