import os
import google.auth
from google.cloud import monitoring_v3

def get_client():
    credentials, project_id = google.auth.default()
    return monitoring_v3.MetricServiceClient(credentials=credentials)

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')