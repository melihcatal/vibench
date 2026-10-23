import boto3

cw = boto3.client('cloudwatch')

def aggregate_metric_stats(metric_name, start_time, end_time):
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
        Period=3600,
        Statistics=['Sum', 'Minimum', 'Maximum', 'SampleCount'],
        Unit='Seconds'
    )
    return response