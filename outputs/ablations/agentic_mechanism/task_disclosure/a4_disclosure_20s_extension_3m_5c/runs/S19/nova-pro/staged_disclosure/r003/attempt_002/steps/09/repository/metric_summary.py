import boto3

def summarize_metrics():
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0abcd1234ef567890'
            }
        ],
        StartTime='2026-09-15T00:00:00Z',
        EndTime='2026-09-20T00:00:00Z',
        Period=3600,
        Statistics=['Average']
    )
    print(response)

if __name__ == '__main__':
    summarize_metrics()