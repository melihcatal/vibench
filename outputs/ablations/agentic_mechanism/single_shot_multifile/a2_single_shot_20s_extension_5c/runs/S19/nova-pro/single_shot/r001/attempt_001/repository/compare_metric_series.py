import boto3

client = boto3.client('cloudwatch')

def compare_metric_series(metric_name, dimension_name, dimension_value1, dimension_value2, start_time, end_time):
    response1 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': dimension_value1
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Seconds'
    )
    response2 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': dimension_value2
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Seconds'
    )
    return response1['Datapoints'], response2['Datapoints']