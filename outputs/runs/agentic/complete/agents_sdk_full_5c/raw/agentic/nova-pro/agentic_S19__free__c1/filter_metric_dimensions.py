import boto3

def filter_metric_dimensions(metric_name, dimension_name, dimension_value, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.list_metrics(
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