import boto3


def metric_summary(
    metric_name: str, start_time: str, end_time: str, namespace: str = "AWS/EC2"
):
    client = boto3.client("cloudwatch")
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Maximum"],
    )
    datapoints = sorted(
        response.get("Datapoints", []), key=lambda x: x.get("Timestamp")
    )
    if not datapoints:
        return {"metric_name": metric_name, "trend": "no_data", "anomalies": []}
    latest = datapoints[-1]
    first = datapoints[0]
    trend = "up" if latest.get("Average", 0) > first.get("Average", 0) else "down"
    anomalies = [
        p for p in datapoints if p.get("Maximum", 0) > latest.get("Average", 0) * 1.5
    ]
    return {"metric_name": metric_name, "trend": trend, "anomalies": anomalies}
