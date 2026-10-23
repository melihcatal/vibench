import boto3
from observability_client import cw_client
from observability_models import MetricData


def filter_metric_dimensions(
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int,
    dimensions: Dict[str, str],
):
    response = cw_client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
    )
    datapoints = response["Datapoints"]
    return [MetricData(dp["Timestamp"].isoformat(), dp["Average"]) for dp in datapoints]
