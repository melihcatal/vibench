import boto3
from datetime import datetime, timedelta

def get_aggregated_metric_statistics(metric_name, namespace, start_time, end_time, period, statistics):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-0123456789abcdef0'
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
        Unit='Seconds'
    )
    return response

if __name__ == '__main__':
    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    start_time = datetime.utcnow() - timedelta(minutes=60)
    end_time = datetime.utcnow()
    period = 300
    statistics = ['Average']
    response = get_aggregated_metric_statistics(metric_name, namespace, start_time, end_time, period, statistics)
    print(response)