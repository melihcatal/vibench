import boto3

def filter_metric_dimensions(namespace, metric_name, dimensions):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        EndTime=datetime.datetime.utcnow(),
        Statistics=['Average']
    )
    return response['Datapoints']