from botocore.exceptions import ClientError

import boto3

cloudwatch = boto3.client('cloudwatch')


def put_metric_data(namespace, metric_data):
    try:
        response = cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )
        return response
    except ClientError as e:
        print(e)
        return None


def get_metric_statistics(namespace, metric_name, dimensions, start_time, end_time, period, statistics):
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics
        )
        return response
    except ClientError as e:
        print(e)
        return None


def normalize_metric_data(metric_data):
    normalized_data = []
    for data in metric_data:
        normalized_data.append({
            'MetricName': data['MetricName'],
            'Value': data['Value'],
            'Timestamp': data['Timestamp'],
            'Unit': data.get('Unit', 'None')
        })
    return normalized_data