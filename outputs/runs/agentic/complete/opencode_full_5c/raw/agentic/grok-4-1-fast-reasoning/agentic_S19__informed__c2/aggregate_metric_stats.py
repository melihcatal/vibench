from datetime import datetime
from typing import Dict, Any
import boto3
from observability_client import create_aws_session
from observability_models import normalize_datapoints


def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = "AWS/EC2",
    period_seconds: int = 300,
) -> Dict[str, Any]:
    session = create_aws_session()
    client = session.client("cloudwatch")
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period_seconds,
        Statistics=["Average", "Sum", "SampleCount", "Minimum", "Maximum"],
    )
    dps = normalize_datapoints(response["Datapoints"])
    if not dps:
        return {}
    values = [d["value"] for d in dps]
    max_vals = [d.get("max", v) for d, v in zip(dps, values)]
    min_vals = [d.get("min", v) for d, v in zip(dps, values)]
    sums = [d.get("sum", v) for d, v in zip(dps, values)]
    return {
        "period_count": len(dps),
        "overall_average": sum(values) / len(values),
        "overall_max": max(max_vals),
        "overall_min": min(min_vals),
        "total_sum": sum(sums),
        "total_samples": sum(d["sample_count"] for d in dps),
    }
