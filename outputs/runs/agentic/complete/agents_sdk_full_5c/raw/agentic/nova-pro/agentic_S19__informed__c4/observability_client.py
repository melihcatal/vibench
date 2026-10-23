import os
from google.cloud import monitoring_v3

def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()

def get_project_name(project_id):
    client = get_monitoring_client()
    return client.common_project_path(project_id)