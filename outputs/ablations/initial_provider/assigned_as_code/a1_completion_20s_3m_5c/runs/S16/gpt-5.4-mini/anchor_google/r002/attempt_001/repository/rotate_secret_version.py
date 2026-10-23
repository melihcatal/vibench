from google.cloud import secretmanager

from security_models import build_secret_path, get_secret_name, get_version_name


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    secret_id = get_secret_name(payload, config)
    version = get_version_name(payload, config)
    name = build_secret_path(config["project_id"], secret_id, version)
    response = client.access_secret_version(request={"name": name})
    return {"secret_version": version, "secret_value": response.payload.data.decode("utf-8")}
