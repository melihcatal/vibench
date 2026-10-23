import boto3

def aggregate_metric_stats(metric_name, namespace, start_time, end_time, period, statistics):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )
    return response
