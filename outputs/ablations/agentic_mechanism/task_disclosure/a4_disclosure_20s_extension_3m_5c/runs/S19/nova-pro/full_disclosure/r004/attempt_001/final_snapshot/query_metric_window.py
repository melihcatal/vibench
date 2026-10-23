import boto3

def query_metric_window(metric_name, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': metric_name,
                        'Dimensions': [{
                            'Name': 'InstanceId',
                            'Value': 'i-0123456789abcdef0'
                        }]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response

if __name__ == '__main__':
    start_time = '2026-09-19T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    metric_name = 'CPUUtilization'
    result = query_metric_window(metric_name, start_time, end_time)
    print(result)