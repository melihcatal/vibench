import boto3

def filter_metric_dimensions(metric_name, dimension_name, dimension_value):
    client = boto3.client('cloudwatch')
    response = client.list_metrics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': dimension_name,
                'Value': dimension_value
            }
        ]
    )
    return response