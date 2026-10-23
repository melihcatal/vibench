import os
from google.cloud import monitoring_v3


def get_client():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    return monitoring_v3.MetricServiceClient()