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
            Statistics=['Average', 'Sum', 'SampleCount']
        )
    else:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Period=3600,
            StartTime=(datetime.utcnow() - timedelta(days=1)),
            EndTime=datetime.utcnow(),
            Statistics=['Average', 'Sum', 'SampleCount']
        )
    
    return response

if __name__ == '__main__':\n    namespace = 'YourNamespace'\n    metric_name = 'YourMetricName'\n    dimensions = [{'Name': 'YourDimensionName', 'Value': 'YourDimensionValue'}]\n    summary = summarize_metric_trends(namespace, metric_name, dimensions)\n    print(summary)