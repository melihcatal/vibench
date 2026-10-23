from google.cloud import secretmanager

from security_client import secret_version_name


def fetch_db_secret(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = secret_version_name(config["project_id"], payload["secret_id"], config.get("version", "latest"))
    response = client.access_secret_version(request={"name": name})
    return {"db_secret": response.payload.data.decode("utf-8")}
