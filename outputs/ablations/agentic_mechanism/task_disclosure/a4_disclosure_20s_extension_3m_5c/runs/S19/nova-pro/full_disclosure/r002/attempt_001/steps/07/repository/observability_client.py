import boto3

class ObservabilityClient:
    def __init__(self, region_name):
        self.client = boto3.client('cloudwatch', region_name=region_name)

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

    def list_metrics(self, namespace=None, metric_name=None, dimensions=None):
        response = self.client.list_metrics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions
        )
        return response

    def put_metric_data(self, namespace, metric_data):
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )
        return response
