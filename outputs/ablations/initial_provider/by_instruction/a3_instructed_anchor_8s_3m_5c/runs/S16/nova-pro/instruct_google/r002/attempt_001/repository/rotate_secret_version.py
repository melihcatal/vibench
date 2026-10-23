from google.cloud import secretmanager

def rotate_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, version_id)
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')