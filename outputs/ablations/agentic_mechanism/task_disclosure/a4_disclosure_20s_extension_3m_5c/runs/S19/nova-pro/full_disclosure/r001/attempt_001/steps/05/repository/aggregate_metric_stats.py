import boto3

def get_aggregated_metric_stats(metric_name, namespace, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
    )
    return response

if __name__ == '__main__':
    metric_name = 'YourMetricName'
    namespace = 'YourNamespace'
    start_time = '2026-09-20T00:00:00Z'
    end_time = '2026-09-20T23:59:59Z'
    stats = get_aggregated_metric_stats(metric_name, namespace, start_time, end_time)
    print(stats)