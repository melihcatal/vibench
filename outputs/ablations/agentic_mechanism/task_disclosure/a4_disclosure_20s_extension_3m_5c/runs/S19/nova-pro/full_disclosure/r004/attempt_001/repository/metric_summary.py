import boto3

def summarize_metrics(namespace, metric_name, period=3600):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'AutoScalingGroupName',
            'Value': 'example-asg'
        }],
        StartTime=(datetime.utcnow() - timedelta(hours=6)),
        EndTime=datetime.utcnow(),
        Period=period,
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
    )
    if response['Datapoints']:
        return response['Datapoints'][-1]
    else:
        return 'No datapoints found'