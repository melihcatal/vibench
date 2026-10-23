import boto3

from observability_client import load_config
from observability_models import normalize_datapoints


def metric_summary(metric_name, start_time, end_time, dimensions=None):
    cfg = load_config()
    client = boto3.client("cloudwatch", region_name=cfg["region_name"])
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Maximum"],
        Dimensions=[{"Name": k, "Value": v} for k, v in (dimensions or {}).items()],
    )
    datapoints = normalize_datapoints(response.get("Datapoints", []))
    return {"count": len(datapoints), "datapoints": datapoints}
