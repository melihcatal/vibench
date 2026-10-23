from google.cloud import secretmanager


def fetch_api_key(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path("my-project", secret_id, "latest")
    response = client.access_secret_version(name)
    return response.payload.data.decode("UTF-8")
