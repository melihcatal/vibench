import boto3

def configure_cloudwatch(region_name):
    return boto3.client('cloudwatch', region_name=region_name)

def put_metric_data(client, namespace, metric_data):
    response = client.put_metric_data(
        Namespace=namespace,
        MetricData=metric_data
    )
    return response

def get_metric_statistics(client, namespace, metric_name, start_time, end_time, period, statistics, dimensions=None):
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
        Dimensions=dimensions
    )
    return response