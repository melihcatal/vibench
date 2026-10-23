from google.cloud import secretmanager

def get_secret_client():
    return secretmanager.SecretManagerServiceClient()