from datetime import datetime, timezone
import time
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


def write_correlated_logs(payload, config=None):
    config = config or {}
    timestamp_ms = payload.get("timestamp_ms", time.time() * 1000)
    request_id = payload["request_id"]
    events = []
    for event in payload["events"]:
        item = dict(event)
        item["request_id"] = request_id
        item["TimeGenerated"] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
        events.append(item)
    with DefaultAzureCredential() as credential:
        with LogsIngestionClient(endpoint=config["endpoint"], credential=credential) as client:
            client.upload(rule_id=config["rule_id"], stream_name=config["stream_name"], logs=events)
    return {"submitted": True, "request_id": request_id, "count": len(events)}
