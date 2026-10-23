import os

from security_client import client, load_config, secret_path
from security_models import decode_bytes


def secret_label_safety() -> bool:
    cfg = load_config(os.environ.get("LABEL_SAFETY_SECRET", "label-safety"))
    response = client().access_secret_version(request={"name": secret_path(cfg)})
    text = decode_bytes(response.payload.data).lower()
    return not any(token in text for token in ("password", "secret", "token", "apikey"))
