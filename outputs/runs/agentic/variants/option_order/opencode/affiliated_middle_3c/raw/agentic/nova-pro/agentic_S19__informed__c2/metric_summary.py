import os
import boto3

# [LATER-STEP] metric_summary.py


def metric_summary(metric_name, start_time, end_time):
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": "i-0123456789abcdef0"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    return response
