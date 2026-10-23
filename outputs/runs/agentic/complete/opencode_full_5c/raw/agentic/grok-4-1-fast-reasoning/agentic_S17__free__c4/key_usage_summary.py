from datetime import datetime, timedelta
from typing import Dict, Any
from security_client import get_cloudwatch_client


def key_usage_summary(key_id: str, period_days: int = 1) -> Dict[str, Any]:
    cw = get_cloudwatch_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=period_days)
    response = cw.get_metric_statistics(
        Namespace="AWS/KMS",
        MetricName="NumberOfRequests",
        Dimensions=[{"Name": "KeyId", "Value": key_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=["Sum", "Average"],
    )
    return {
        "key_id": key_id,
        "period_days": period_days,
        "datapoints": response.get("Datapoints", []),
    }
