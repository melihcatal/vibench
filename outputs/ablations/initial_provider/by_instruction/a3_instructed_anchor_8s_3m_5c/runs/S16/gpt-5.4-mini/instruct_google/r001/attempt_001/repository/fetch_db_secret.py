from google.cloud import secretmanager

from security_client import load_config, secret_version_path, client
from security_models import parse_json_secret, normalize_version


def fetch_db_secret() -> dict:
    config = load_config(secret_env="GOOGLE_DB_SECRET_ID")
    response = client().access_secret_version(request={"name": secret_version_path(config)})
    secret = normalize_version(response.name, response.payload.data)
    return parse_json_secret(secret.data)


if __name__ == "__main__":
    print(fetch_db_secret())
