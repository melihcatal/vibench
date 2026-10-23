import boto3

cw = boto3.client('cloudwatch')

def filter_metric_dimensions(metric_name, dimension_name, dimension_value, start_time, end_time):
    response = cw.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': dimension_name,
                'Value': dimension_value
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response