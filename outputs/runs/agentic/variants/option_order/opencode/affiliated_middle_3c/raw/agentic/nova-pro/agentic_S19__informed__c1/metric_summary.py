import boto3


def metric_summary(metric_name, start_time, end_time):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/CloudWatch",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": "i-0abcd1234ef567890"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Sum", "SampleCount"],
    )
    return response
