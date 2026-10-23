import boto3

def query_metric_window(metric_name, start_time, end_time, namespace='AWS/CloudWatch'):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response['Datapoints'] if 'Datapoints' in response else []