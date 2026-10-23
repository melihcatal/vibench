import base64
import json

from security_client import load_security_config, request_json, secret_manager_base_url
from security_models import normalize_secret_name


def parse_json_secret(secret_id: str = "app-settings"):
    config = load_security_config()
    secret_id = normalize_secret_name(secret_id)
    url = f"{secret_manager_base_url(config)}/{secret_id}/versions/latest:access"
    response = request_json("GET", url)
    data = response.get("payload", {}).get("data", "")
    raw = base64.b64decode(data).decode("utf-8") if data else "{}"
    return json.loads(raw)


if __name__ == "__main__":
    print(parse_json_secret())
