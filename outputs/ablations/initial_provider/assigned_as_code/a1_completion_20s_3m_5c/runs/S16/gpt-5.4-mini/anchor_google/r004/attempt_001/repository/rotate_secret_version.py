from google.cloud import secretmanager

from security_client import secret_version_name


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    version = payload.get("version") or config.get("version", "latest")
    name = secret_version_name(config["project_id"], payload["secret_id"], version)
    response = client.access_secret_version(request={"name": name})
    return {"rotated_secret": response.payload.data.decode("utf-8"), "version": version}
