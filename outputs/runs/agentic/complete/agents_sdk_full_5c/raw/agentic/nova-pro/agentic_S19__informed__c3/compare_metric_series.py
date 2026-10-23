import boto3

def compare_metric_series(metric_name, dimension_name, dimension_value1, dimension_value2, start_time, end_time):
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
                            'Name': dimension_name,
                            'Value': dimension_value1
                        }]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            },
            {
                'Id': 'm2',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': metric_name,
                        'Dimensions': [{
                            'Name': dimension_name,
                            'Value': dimension_value2
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