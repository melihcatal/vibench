import os
from google.cloud import monitoring_v3

def get_client():
    return monitoring_v3.MetricServiceClient()

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')
