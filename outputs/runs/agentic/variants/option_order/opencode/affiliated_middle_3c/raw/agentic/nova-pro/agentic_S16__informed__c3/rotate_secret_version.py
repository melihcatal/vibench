from google.cloud import secretmanager


def rotate_secret_version(secret_id, version):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path("my-project", secret_id, version)
    response = client.access_secret_version(name)
    return response.payload.data.decode("UTF-8")
