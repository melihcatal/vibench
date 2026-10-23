import boto3

def query_metric_data(namespace, metric_name, dimensions, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    return response['Datapoints'] if 'Datapoints' in response else []

if __name__ == '__main__':
    namespace = 'AWS/EC2'
    metric_name = 'CPUUtilization'
    dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    datapoints = query_metric_data(namespace, metric_name, dimensions, start_time, end_time)
    print(datapoints)