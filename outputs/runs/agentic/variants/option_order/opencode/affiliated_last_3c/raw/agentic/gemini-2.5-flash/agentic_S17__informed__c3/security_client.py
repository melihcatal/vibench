from google.cloud import kms


def get_kms_client():
    return kms.KeyManagementServiceClient()
