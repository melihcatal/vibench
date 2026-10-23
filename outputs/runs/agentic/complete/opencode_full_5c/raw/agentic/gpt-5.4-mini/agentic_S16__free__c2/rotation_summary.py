from security_client import load_security_config, request_json, secret_manager_base_url
from security_models import SecretRotationSummary, normalize_secret_name


def rotation_summary(secret_id: str = "api-key") -> SecretRotationSummary:
    config = load_security_config()
    secret_id = normalize_secret_name(secret_id)
    url = f"{secret_manager_base_url(config)}/{secret_id}/versions/latest"
    response = request_json("GET", url)
    return SecretRotationSummary(
        secret_id=secret_id,
        version=response.get("name", "latest"),
        state=response.get("state", "UNKNOWN"),
    )


if __name__ == "__main__":
    print(rotation_summary())
