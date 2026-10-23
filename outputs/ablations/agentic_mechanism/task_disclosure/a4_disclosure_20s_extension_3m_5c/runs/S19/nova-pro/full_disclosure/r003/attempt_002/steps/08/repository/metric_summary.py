import boto3

def summarize_metric_trends(namespace, metric_name, dimensions=None):
    cloudwatch = boto3.client('cloudwatch')
    
    if dimensions:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            Period=3600,
            StartTime=(datetime.utcnow() - timedelta(days=1)),
            EndTime=datetime.utcnow(),
            Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
        )
    else:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Period=3600,
            StartTime=(datetime.utcnow() - timedelta(days=1)),
            EndTime=datetime.utcnow(),
            Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
        )
    
    return response

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    summary = summarize_metric_trends(namespace, metric_name, dimensions)
    print(summary)