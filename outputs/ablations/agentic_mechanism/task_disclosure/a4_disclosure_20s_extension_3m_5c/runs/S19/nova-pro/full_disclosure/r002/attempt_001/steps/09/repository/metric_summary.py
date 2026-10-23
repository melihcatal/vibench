import boto3

def summarize_metric_trends(namespace, metric_name, period=3600, start_time=None, end_time=None):
    cloudwatch = boto3.client('cloudwatch')
    if not start_time or not end_time:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0abcd1234ef567890'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
    )
    return response

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    summary = summarize_metric_trends(namespace, metric_name)
    print(summary)