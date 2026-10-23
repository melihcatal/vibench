import boto3

def query_metric_window(metric_name, start_time, end_time, namespace='AWS/EC2'):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Period=60,
        StartTime=start_time,
        EndTime=end_time,
        MetricName=metric_name,
        Namespace=namespace,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response['Datapoints']

if __name__ == '__main__':
    metric_name = 'CPUUtilization'
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    datapoints = query_metric_window(metric_name, start_time, end_time)
    for dp in datapoints:
        print(dp)