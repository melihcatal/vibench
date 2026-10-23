import boto3

def get_aggregated_metric_stats(namespace, metric_name, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0123456789abcdef0'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum'],
        Unit='Seconds'
    )
    return response

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    stats = get_aggregated_metric_stats(namespace, metric_name, start_time, end_time)
    print(stats)