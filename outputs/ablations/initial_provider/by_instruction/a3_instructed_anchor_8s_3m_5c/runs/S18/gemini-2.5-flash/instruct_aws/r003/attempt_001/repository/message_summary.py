import boto3

def summarize_message_processing(metric_namespace: str, metric_name: str, value: float, dimensions: list[dict] = None):
    cloudwatch_client = boto3.client('cloudwatch')  # AWS SDK import
    metric_data = [
        {
            'MetricName': metric_name,
            'Value': value,
            'Unit': 'Count',
        },
    ]
    if dimensions:
        metric_data[0]['Dimensions'] = dimensions

    response = cloudwatch_client.put_metric_data(
        Namespace=metric_namespace,
        MetricData=metric_data
    )
    return response
