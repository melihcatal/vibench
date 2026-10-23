import boto3
from observability_client import get_cloudwatch_client

cw = get_cloudwatch_client()

def metric_summary(metric_name, start_time, end_time):
    response = cw.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0abcd1234ef567890'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average', 'Sum', 'SampleCount'],
        Unit='Seconds'
    )
    return response