import os
import json

from google.cloud import monitoring_v3

def get_client():
    project_id = os.getenv('GCP_PROJECT_ID')
    return monitoring_v3.MetricServiceClient(project=project_id)

def normalize_payload(payload):
    return json.dumps(payload)
