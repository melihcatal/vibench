import base64
from typing import Any

from security_client import load_security_config, request_json, secret_manager_base_url
from security_models import SecretFetchRequest, normalize_secret_name


def fetch_api_key(secret_id: str = "api-key") -> str:
    config = load_security_config()
    request = SecretFetchRequest(secret_id=normalize_secret_name(secret_id))
    url = f"{secret_manager_base_url(config)}/{request.secret_id}/versions/{request.version}:access"
    response = request_json("GET", url)
    data = response.get("payload", {}).get("data", "")
    if data:
        return base64.b64decode(data).decode("utf-8")
    return ""


if __name__ == "__main__":
    print(fetch_api_key())
