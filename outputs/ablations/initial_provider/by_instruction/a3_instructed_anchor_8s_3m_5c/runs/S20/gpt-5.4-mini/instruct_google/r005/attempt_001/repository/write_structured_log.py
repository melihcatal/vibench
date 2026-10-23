from observability_client import client_for_project, load_config
from observability_models import LogRecord, build_structured_payload


def write_structured_log(message: str, severity: str = "INFO", labels=None, payload=None):
    cfg = load_config()
    client = client_for_project(cfg.project_id)
    logger = client.logger(cfg.log_name)
    record = LogRecord(message=message, severity=severity, labels=labels or {}, payload=payload or {})
    logger.log_struct(build_structured_payload(record), severity=record.severity, labels=record.labels, timestamp=record.timestamp)
    return {"project_id": cfg.project_id, "log_name": cfg.log_name, "severity": record.severity}
