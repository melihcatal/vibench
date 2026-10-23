import os

from security_client import client, load_config, secret_path
from security_models import decode_bytes


def rotation_summary() -> str:
    cfg = load_config(os.environ.get("ROTATION_SUMMARY_SECRET", "rotation-summary"))
    response = client().access_secret_version(request={"name": secret_path(cfg)})
    return decode_bytes(response.payload.data)
