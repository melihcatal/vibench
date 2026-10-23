import boto3

def filter_metric_dimensions(namespace, metric_name, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.list_metrics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-1234567890abcdef0'
            }
        ]
    )
    return response