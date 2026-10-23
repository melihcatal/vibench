from google.cloud import secretmanager


def fetch_api_key(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, "latest")
    response = client.access_secret_version(name)
    return response.payload.data.decode("UTF-8")
