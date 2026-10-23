from google.cloud import storage

def get_storage_client():
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('path/to/service_account.json')
    return storage.Client(credentials=credentials)