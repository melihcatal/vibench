import os

import boto3


def metric_summary(metric_name, start_time, end_time, namespace=None):
    client = boto3.client(
        "cloudwatch",
        region_name=os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
    )
    response = client.get_metric_statistics(
        Namespace=namespace
        or os.getenv("CLOUDWATCH_NAMESPACE")
        or "ManagedMetricsMonitoring",
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Minimum", "Maximum"],
    )
    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return {"metric_name": metric_name, "trend": "unknown", "anomalies": []}
    averages = [
        point.get("Average") for point in datapoints if point.get("Average") is not None
    ]
    trend = "stable"
    if len(averages) >= 2 and averages[-1] > averages[0]:
        trend = "increasing"
    elif len(averages) >= 2 and averages[-1] < averages[0]:
        trend = "decreasing"
    anomalies = [
        point
        for point in datapoints
        if point.get("Maximum", 0) > point.get("Average", 0) * 1.5
        if point.get("Average")
    ]
    return {"metric_name": metric_name, "trend": trend, "anomalies": anomalies}
