from google.cloud import secretmanager

from security_client import load_config, secret_version_path, client
from security_models import normalize_version


def read_secret_version() -> str:
    config = load_config(secret_env="GOOGLE_ROTATE_SECRET_ID", version_env="GOOGLE_SECRET_VERSION")
    response = client().access_secret_version(request={"name": secret_version_path(config)})
    secret = normalize_version(response.name, response.payload.data)
    return secret.data


if __name__ == "__main__":
    print(read_secret_version())
