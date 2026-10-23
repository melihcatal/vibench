from datetime import datetime, timedelta
from security_client import get_cloudwatch_client


def key_usage_summary(key_id: str, hours: int = 24) -> dict:
    client = get_cloudwatch_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    dimensions = [{"Name": "KeyId", "Value": key_id}]
    metrics = [
        {"name": "NumberOfBytesEncrypted", "stats": ["Sum"]},
        {"name": "NumberOfBytesDecrypted", "stats": ["Sum"]},
        {"name": "RequestCount", "stats": ["Sum"]},
    ]
    summary = {}
    for m in metrics:
        resp = client.get_metric_statistics(
            Namespace="AWS/KMS",
            MetricName=m["name"],
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=m["stats"],
        )
        summary[m["name"]] = resp.get("Datapoints", [])
    return summary
