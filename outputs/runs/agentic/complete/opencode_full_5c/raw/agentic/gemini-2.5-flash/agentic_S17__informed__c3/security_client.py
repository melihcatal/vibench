from google.cloud import kms_v1
import os


def get_kms_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.
    # The client will automatically pick up credentials from the environment.
    return kms_v1.KeyManagementServiceClient()
