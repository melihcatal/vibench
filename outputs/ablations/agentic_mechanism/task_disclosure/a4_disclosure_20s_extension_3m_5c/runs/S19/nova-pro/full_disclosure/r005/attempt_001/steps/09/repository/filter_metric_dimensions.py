import boto3

def filter_metric_dimensions(namespace, metric_name, dimension_name, dimension_value):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': dimension_name,
                'Value': dimension_value
            }
        ],
        StartTime='2026-09-15T00:00:00Z',
        EndTime='2026-09-20T00:00:00Z',
        Period=3600,
        Statistics=['Average']
    )
    return response
