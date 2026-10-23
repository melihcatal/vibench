import boto3
from typing import List, Dict, Any, Optional
from observability_client import get_aws_region, make_dimensions, create_recent_window
from observability_models import parse_datapoints, MetricDatapoint


def aggregate_metric_stats(
    metric_name: str,
    duration_minutes: int = 60,
    namespace: str = "AWS/EC2",
    period: int = 300,
    statistics: List[str] = ["Sum", "Average", "SampleCount", "Minimum", "Maximum"],
    dimensions: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, float]:
    region = get_aws_region()
    client = boto3.client("cloudwatch", region_name=region)
    window = create_recent_window(duration_minutes)
    dims = make_dimensions(dimensions)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=window["start"],
        EndTime=window["end"],
        Period=period,
        Statistics=statistics,
        Dimensions=dims,
    )
    points = parse_datapoints(response["Datapoints"])
    if not points:
        return {}
    total_sum = sum(p.sum_ or 0 for p in points)
    total_samples = sum(p.sample_count or 0 for p in points)
    overall_avg = total_sum / total_samples if total_samples > 0 else 0.0
    min_val = min((p.minimum or float("inf") for p in points), default=0.0)
    max_val = max((p.maximum or float("-inf") for p in points), default=0.0)
    return {
        "overall_average": overall_avg,
        "total_sum": total_sum,
        "total_samples": total_samples,
        "min_value": min_val,
        "max_value": max_val,
    }
