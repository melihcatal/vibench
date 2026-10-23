import boto3

def filter_metric_dimensions(namespace, metric_name, dimensions):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        Period=300,
        Statistics=['Average'],
        Unit='Count'
    )
    return response
