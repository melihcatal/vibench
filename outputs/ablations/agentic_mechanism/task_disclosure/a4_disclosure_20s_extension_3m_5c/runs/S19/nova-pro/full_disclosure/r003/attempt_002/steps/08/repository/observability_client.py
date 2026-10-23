import boto3

class ObservabilityClient:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')

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

    def list_metrics(self, namespace=None, metric_name=None, dimensions=None):
        response = self.cloudwatch.list_metrics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions
        )
        return response