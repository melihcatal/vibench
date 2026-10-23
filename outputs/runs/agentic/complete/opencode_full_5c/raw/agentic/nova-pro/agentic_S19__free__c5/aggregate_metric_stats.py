import boto3
from observability_client import cw_client
from observability_models import MetricStatistics


def aggregate_metric_stats(
    metric_name: str, start_time: str, end_time: str, period: int
):
    response = cw_client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Minimum", "Maximum", "Sum", "SampleCount", "Average"],
    )
    stats = response["Datapoints"][0]
    return MetricStatistics(
        stats["Minimum"],
        stats["Maximum"],
        stats["Sum"],
        stats["SampleCount"],
        stats["Average"],
    )
