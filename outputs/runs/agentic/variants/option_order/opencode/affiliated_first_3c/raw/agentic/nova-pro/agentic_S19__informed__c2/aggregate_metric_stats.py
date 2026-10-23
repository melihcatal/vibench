import boto3


def aggregate_metric_stats(metric_name, start_time, end_time):
    client = boto3.client("cloudwatch")
    response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Sum", "SampleCount"],
        Unit="Seconds",
    )
    return response
