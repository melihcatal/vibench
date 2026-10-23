import boto3
from observability_models import MetricDatapoint

client = boto3.client('cloudwatch')

def summarize_metric(metric_name, start_time, end_time):
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-1234567890abcdef0'
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Seconds'
    )
    datapoints = [MetricDatapoint(dp['Timestamp'], dp['Average']) for dp in response['Datapoints']]
    return datapoints