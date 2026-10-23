from google.cloud import secretmanager


def security_client():
    return secretmanager.SecretManagerServiceClient()
