from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

from observability_models import build_correlation_event, build_log_event


def write_correlated_logs(payload, config=None):
    config = config or {}
    correlation_id = payload["correlation_id"]
    logs = []
    for item in payload["events"]:
        event = build_log_event(item)
        event.update(build_correlation_event({"correlation_id": correlation_id}))
        logs.append(event)
    with DefaultAzureCredential() as credential:
        with LogsIngestionClient(endpoint=config["endpoint"], credential=credential) as client:
            client.upload(rule_id=config["rule_id"], stream_name=config["stream_name"], logs=logs)
    return {"submitted": True, "count": len(logs)}
