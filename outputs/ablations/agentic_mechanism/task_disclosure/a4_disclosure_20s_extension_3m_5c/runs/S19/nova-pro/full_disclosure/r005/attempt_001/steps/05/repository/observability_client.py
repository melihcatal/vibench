import boto3

class ObservabilityClient:
    def __init__(self, region_name):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)

    def get_metric_statistics(self, namespace, metric_name, dimensions, start_time, end_time, period, statistics):
        response = self.cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics
        )
        return response

    def put_metric_data(self, namespace, metric_data):
        response = self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )
        return response