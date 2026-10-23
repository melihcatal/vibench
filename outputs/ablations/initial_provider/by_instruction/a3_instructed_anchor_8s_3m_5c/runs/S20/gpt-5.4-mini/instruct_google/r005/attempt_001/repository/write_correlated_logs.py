from observability_client import client_for_project, load_config
from observability_models import LogRecord, build_structured_payload


def write_correlated_logs(messages, correlation_id, severity="INFO"):
    cfg = load_config()
    client = client_for_project(cfg.project_id)
    logger = client.logger(cfg.log_name)
    results = []
    for message in messages:
        record = LogRecord(message=message, severity=severity, labels={"correlation_id": correlation_id}, payload={"correlation_id": correlation_id})
        logger.log_struct(build_structured_payload(record), severity=record.severity, labels=record.labels, timestamp=record.timestamp)
        results.append({"message": message, "correlation_id": correlation_id})
    return results
