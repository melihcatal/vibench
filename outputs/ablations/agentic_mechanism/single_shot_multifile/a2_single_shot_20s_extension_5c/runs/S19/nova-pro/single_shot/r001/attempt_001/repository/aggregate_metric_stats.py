import boto3

client = boto3.client('cloudwatch')

def aggregate_metric_stats(metric_name, start_time, end_time):
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-1234567890abcdef0'
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum', 'Minimum', 'Maximum', 'SampleCount'],
        Unit='Seconds'
    )
    return response