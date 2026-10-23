import boto3


def metric_summary(metric_name, start_time, end_time):
    client = boto3.client("cloudwatch")
    response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    return response
