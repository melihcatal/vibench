import boto3

def summarize_metric_trends(namespace, metric_name, dimensions=None):
    cloudwatch = boto3.client('cloudwatch')
    
    if dimensions:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            Period=300,
            StartTime=(datetime.utcnow() - timedelta(hours=1)),
            EndTime=datetime.utcnow(),
            Statistics=['Average', 'Sum']
        )
    else:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Period=300,
            StartTime=(datetime.utcnow() - timedelta(hours=1)),
            EndTime=datetime.utcnow(),
            Statistics=['Average', 'Sum']
        )
    
    datapoints = response['Datapoints']
    if datapoints:
        average_values = [dp['Average'] for dp in datapoints if 'Average' in dp]
        sum_values = [dp['Sum'] for dp in datapoints if 'Sum' in dp]
        
        average_trend = sum(average_values) / len(average_values) if average_values else None
        sum_trend = sum(sum_values) / len(sum_values) if sum_values else None
        
        return {
            'average_trend': average_trend,
            'sum_trend': sum_trend,
            'datapoints': datapoints
        }
    else:
        return {'message': 'No datapoints found'}

if __name__ == '__main__':
    namespace = 'YourNamespace'
    metric_name = 'YourMetricName'
    dimensions = [{'Name': 'YourDimensionName', 'Value': 'YourDimensionValue'}]
    summary = summarize_metric_trends(namespace, metric_name, dimensions)
    print(summary)