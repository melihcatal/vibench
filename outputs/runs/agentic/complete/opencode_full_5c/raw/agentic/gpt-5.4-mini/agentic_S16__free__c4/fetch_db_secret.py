import os

from security_client import client, load_config, secret_path
from security_models import decode_bytes, normalize_text


def fetch_db_secret() -> str:
    cfg = load_config(os.environ.get("DB_SECRET_NAME", "db-connection"))
    response = client().access_secret_version(request={"name": secret_path(cfg)})
    return normalize_text(decode_bytes(response.payload.data))
