import boto3

def get_aggregated_metric_stats(namespace, metric_name, start_time, end_time, period):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': 'my-asg'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
    )
    return response

if __name__ == '__main__':
    namespace = 'AWS/AutoScaling'
    metric_name = 'CPUUtilization'
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    period = 300
    stats = get_aggregated_metric_stats(namespace, metric_name, start_time, end_time, period)
    print(stats)