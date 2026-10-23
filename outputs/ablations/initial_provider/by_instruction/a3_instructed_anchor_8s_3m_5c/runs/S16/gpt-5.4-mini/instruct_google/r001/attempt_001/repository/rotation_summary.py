from google.cloud import secretmanager

from security_client import load_config, secret_path, client


def rotation_summary() -> dict:
    config = load_config(secret_env="GOOGLE_ROTATION_SECRET_ID")
    secret = client().get_secret(request={"name": secret_path(config)})
    return {"name": secret.name, "rotation": bool(secret.rotation)}


if __name__ == "__main__":
    print(rotation_summary())
