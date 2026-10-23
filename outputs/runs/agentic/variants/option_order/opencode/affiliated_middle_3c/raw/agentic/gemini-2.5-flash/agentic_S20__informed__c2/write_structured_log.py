from observability_client import get_logging_client
import datetime


def write_structured_log(log_name: str, message: str, severity: str, metadata: dict):
    client = get_logging_client()
    logger = client.logger(log_name)
    logger.log_struct(
        {
            "message": message,
            "severity": severity,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            **metadata,
        }
    )
