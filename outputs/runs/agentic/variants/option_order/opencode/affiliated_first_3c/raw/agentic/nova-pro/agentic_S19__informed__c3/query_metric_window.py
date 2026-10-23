import boto3


def query_metric_window(metric_name, start_time, end_time):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    return response
