from datetime import datetime, timezone
from typing import Dict, Any

from observability_client import CloudWatchClient
from observability_models import AggregatedMetricStats

def aggregate_metric_stats(payload: Dict[str, Any], config: Dict[str, Any] = None) -> AggregatedMetricStats:
    client_wrapper = CloudWatchClient(region_name=config.get("region") if config else None)
    cloudwatch_config = client_wrapper.get_cloudwatch_config(config)
    client = client_wrapper.get_client()

    response = client.get_metric_statistics(
        Namespace=cloudwatch_config["namespace"],
        MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in cloudwatch_config.get("dimensions", {}).items() if v is not None],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cloudwatch_config.get("period_seconds", 60),
        Statistics=payload.get("statistics", ["Average", "Sum", "Minimum", "Maximum", "SampleCount"])
    )

    if response["Datapoints"]:
        # CloudWatch can return multiple datapoints if the period is too short for the time window.
        # For aggregated stats over the *entire* window, we should typically get one datapoint
        # if StartTime/EndTime covers exactly one period for the chosen statistics.
        # We'll take the first one for simplicity, assuming the period is set appropriately.
        datapoint = response["Datapoints"][0]
        return AggregatedMetricStats(
            minimum=float(datapoint.get("Minimum", 0.0)),
            maximum=float(datapoint.get("Maximum", 0.0)),
            average=float(datapoint.get("Average", 0.0)),
            sum=float(datapoint.get("Sum", 0.0)),
            sample_count=float(datapoint.get("SampleCount", 0.0))
        )
    else:
        return AggregatedMetricStats(minimum=0.0, maximum=0.0, average=0.0, sum=0.0, sample_count=0.0)
