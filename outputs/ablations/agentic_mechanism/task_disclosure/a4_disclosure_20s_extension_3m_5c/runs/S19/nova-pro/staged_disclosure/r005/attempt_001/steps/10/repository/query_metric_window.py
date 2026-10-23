import boto3

def query_metric_window(metric_name, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0abcd1234ef567890'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=['Average']
    )
    return response['Datapoints']

if __name__ == '__main__':
    metric_name = 'CPUUtilization'
    start_time = '2026-09-15T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    datapoints = query_metric_window(metric_name, start_time, end_time)
    print(datapoints)