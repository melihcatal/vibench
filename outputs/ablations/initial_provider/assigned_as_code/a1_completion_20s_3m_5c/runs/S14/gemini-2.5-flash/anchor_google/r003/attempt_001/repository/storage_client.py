from google.cloud import storage

def get_storage_client(project_id):
    return storage.Client(project=project_id)
