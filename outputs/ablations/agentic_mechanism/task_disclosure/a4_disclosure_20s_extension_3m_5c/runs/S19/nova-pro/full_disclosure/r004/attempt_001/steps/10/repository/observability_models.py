from botocore.exceptions import ClientError

class ObservabilityModels:
    def __init__(self, cloudwatch_client):
        self.cloudwatch_client = cloudwatch_client

    def create_metric_request(self, namespace, metric_name, dimensions, value, unit):
        return {
            'Namespace': namespace,
            'MetricData': [{
                'MetricName': metric_name,
                'Dimensions': dimensions,
                'Value': value,
                'Unit': unit
            }]
        }

    def normalize_metric_response(self, response):
        if 'MetricData' in response:
            return response['MetricData'][0]
        else:
            raise ClientError({'Error': {'Code': 'InvalidResponse', 'Message': 'Response does not contain MetricData'}}, 'get_metric_data')

    def create_get_metric_request(self, namespace, metric_name, dimensions, start_time, end_time, period, statistics):
        return {
            'Namespace': namespace,
            'MetricName': metric_name,
            'Dimensions': dimensions,
            'StartTime': start_time,
            'EndTime': end_time,
            'Period': period,
            'Statistics': statistics
        }