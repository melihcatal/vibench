from google.cloud import secretmanager

def get_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()
