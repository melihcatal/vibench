import os
from google.cloud import monitoring_v3

def get_client():
    return monitoring_v3.MetricServiceClient()

def get_project_name():
    return monitoring_v3.MetricServiceClient().project_path(os.getenv('GCP_PROJECT_ID'))