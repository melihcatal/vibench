from google.cloud import secretmanager


def build_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def secret_version_name(project_id, secret_id, version="latest"):
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def access_secret_text(client, name):
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
