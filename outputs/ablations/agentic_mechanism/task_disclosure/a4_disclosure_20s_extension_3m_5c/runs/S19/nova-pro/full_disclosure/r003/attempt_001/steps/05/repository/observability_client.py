import boto3

class ObservabilityClient:
    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def get_metric_statistics(self, namespace, metric_name, dimensions, start_time, end_time, period, statistics):
        response = self.client.get_metric_statistics(
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
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )
        return response