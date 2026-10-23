from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self):
        self.monitoring_client = monitoring_v3.MetricServiceClient()

    def get_monitoring_client(self) -> monitoring_v3.MetricServiceClient:
        return self.monitoring_client
