import boto3

cw_client = boto3.client("cloudwatch")


def aggregate_metric_stats(metric_name, start_time, end_time):
    response = cw_client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Sum"],
    )
    return response
