import os

from security_client import client, load_config, secret_path
from security_models import decode_bytes


def rotate_secret_version(version: str = "latest") -> str:
    cfg = load_config(
        os.environ.get("ROTATE_SECRET_NAME", "rotation-target"), version=version
    )
    response = client().access_secret_version(request={"name": secret_path(cfg)})
    return decode_bytes(response.payload.data)
