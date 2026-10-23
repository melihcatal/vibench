from google.cloud import storage

def get_storage_client():
    from google.auth import default
    credentials, project = default()
    storage_client = storage.Client(credentials=credentials, project=project)
    return storage_client
