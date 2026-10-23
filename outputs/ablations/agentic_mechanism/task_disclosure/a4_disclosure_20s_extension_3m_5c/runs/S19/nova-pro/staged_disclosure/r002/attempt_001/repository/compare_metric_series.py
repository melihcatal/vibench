import boto3

def compare_metric_series(namespace, metric_name, dimension_name, resource1, resource2, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')

    response1 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': resource1
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    response2 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': resource2
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    print(f'Metrics for {resource1}: {response1}')
    print(f'Metrics for {resource2}: {response2}')

# Example usage
# compare_metric_series('AWS/EC2', 'CPUUtilization', 'InstanceId', 'i-1234567890abcdef0', 'i-0abcdef1234567890', '2026-09-19T00:00:00Z', '2026-09-20T00:00:00Z')