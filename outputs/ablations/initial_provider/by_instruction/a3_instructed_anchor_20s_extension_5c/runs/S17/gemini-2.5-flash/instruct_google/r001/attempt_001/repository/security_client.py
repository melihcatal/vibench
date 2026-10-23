from google.cloud import kms_v1

def get_kms_client():
    return kms_v1.KeyManagementServiceClient()
