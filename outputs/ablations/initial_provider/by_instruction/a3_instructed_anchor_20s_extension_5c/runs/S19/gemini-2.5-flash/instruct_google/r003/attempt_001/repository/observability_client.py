from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()

    def get_metric_service_client(self):
        return self.client