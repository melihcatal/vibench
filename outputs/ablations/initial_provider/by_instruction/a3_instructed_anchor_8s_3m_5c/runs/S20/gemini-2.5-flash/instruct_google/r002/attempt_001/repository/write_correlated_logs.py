from google.cloud import logging

def write_correlated_logs(log_name: str, correlation_id: str, entries: list):
    """
    Writes multiple application log events that include a shared request or correlation identifier.

    Args:
        log_name (str): The name of the log to write to.
        correlation_id (str): A shared identifier for correlated log entries.
        entries (list): A list of dictionaries, where each dictionary represents a log entry
                        with 'message' and optionally 'severity' and other fields.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    for entry in entries:
        payload = {
            "correlation_id": correlation_id,
            "message": entry.get("message"),
            "severity": entry.get("severity", "INFO"),
            **{k: v for k, v in entry.items() if k not in ["message", "severity"]}
        }
        logger.log_struct(payload, severity=payload["severity"])
