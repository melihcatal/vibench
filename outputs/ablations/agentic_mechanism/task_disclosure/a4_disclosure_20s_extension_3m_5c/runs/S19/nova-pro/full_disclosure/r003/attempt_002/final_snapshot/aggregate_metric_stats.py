import boto3

def get_aggregated_metric_stats(metric_name, namespace, start_time, end_time, period, statistics):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
    )
    return response

if __name__ == '__main__':
    metric_name = 'SampleMetric'
    namespace = 'SampleNamespace'
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    period = 300
    statistics = ['Average', 'Sum']
    stats = get_aggregated_metric_stats(metric_name, namespace, start_time, end_time, period, statistics)
    print(stats)