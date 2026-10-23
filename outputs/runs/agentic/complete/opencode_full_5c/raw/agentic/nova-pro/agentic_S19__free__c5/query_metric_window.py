import boto3
from observability_client import cw_client
from observability_models import MetricData


def query_metric_window(metric_name: str, start_time: str, end_time: str, period: int):
    response = cw_client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
    )
    datapoints = response["Datapoints"]
    return [MetricData(dp["Timestamp"].isoformat(), dp["Average"]) for dp in datapoints]
