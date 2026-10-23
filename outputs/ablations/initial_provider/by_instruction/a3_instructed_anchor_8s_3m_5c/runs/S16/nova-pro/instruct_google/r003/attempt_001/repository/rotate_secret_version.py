from google.cloud import secretmanager

def rotate_secret_version(project_id, secret_id, version):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')