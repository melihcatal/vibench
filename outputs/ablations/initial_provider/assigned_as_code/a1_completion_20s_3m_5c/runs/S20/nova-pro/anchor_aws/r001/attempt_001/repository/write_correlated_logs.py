import boto3

import observability_client
import observability_models


def write_correlated_logs(payloads, config=None):
    config = config or {}
    client = observability_client.get_client(config)
    for payload in payloads:
        response = client.put_log_events(
            logGroupName=config["log_group"],
            logStreamName=config["log_stream"],
            logEvents=[{
                "timestamp": int(payload.get("timestamp_ms", time.time() * 1000)),
                "message": json.dumps(payload["event"]),
            }],
        )
        if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
            raise RuntimeError("The logging service rejected the event")
    return {"submitted": True}