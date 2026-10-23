import json

from google.cloud import secretmanager

from security_client import secret_version_name


def parse_json_secret(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = secret_version_name(config["project_id"], payload["secret_id"], config.get("version", "latest"))
    response = client.access_secret_version(request={"name": name})
    value = json.loads(response.payload.data.decode("utf-8"))
    return {"secret": value}
