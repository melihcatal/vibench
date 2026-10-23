import boto3


def write_correlated_logs(payload, config=None):
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))
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