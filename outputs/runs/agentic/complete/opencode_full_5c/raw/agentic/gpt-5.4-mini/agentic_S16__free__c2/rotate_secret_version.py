import base64

from security_client import load_security_config, request_json, secret_manager_base_url
from security_models import (
    SecretRotationRequest,
    normalize_secret_name,
    normalize_stage,
)


def rotate_secret_version(secret_id: str = "api-key", stage: str = "latest") -> str:
    config = load_security_config()
    request = SecretRotationRequest(
        secret_id=normalize_secret_name(secret_id), stage=normalize_stage(stage)
    )
    url = f"{secret_manager_base_url(config)}/{request.secret_id}/versions/{request.stage}:access"
    response = request_json("GET", url)
    data = response.get("payload", {}).get("data", "")
    return base64.b64decode(data).decode("utf-8") if data else ""


if __name__ == "__main__":
    print(rotate_secret_version())
