import os
from google.cloud import monitoring_v3

def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()
