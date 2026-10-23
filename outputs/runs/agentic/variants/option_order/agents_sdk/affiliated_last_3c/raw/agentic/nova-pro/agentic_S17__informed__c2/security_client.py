import os
from google.cloud import kms

def get_kms_client():
    return kms.KeyManagementServiceClient()

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')