import os

from google.cloud import monitoring_v3

def get_config():
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id'),
        'period_seconds': int(os.getenv('PERIOD_SECONDS', 60))
    }

def create_client():
    return monitoring_v3.MetricServiceClient()