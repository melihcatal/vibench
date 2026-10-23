import boto3

def compare_metric_statistics(namespace, metric_name, dimension_name, dimension_values, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    
    statistics = []
    for value in dimension_values:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=[{
                'Name': dimension_name,
                'Value': value
            }],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        statistics.append((value, response['Datapoints']))
    
    return statistics

# Example usage
namespace = 'AWS/EC2'
metric_name = 'CPUUtilization'
dimension_name = 'InstanceId'
dimension_values = ['i-1234567890abcdef0', 'i-0abcdef1234567890']
start_time = '2026-09-19T00:00:00Z'
end_time = '2026-09-20T00:00:00Z'

statistics = compare_metric_statistics(namespace, metric_name, dimension_name, dimension_values, start_time, end_time)
print(statistics)