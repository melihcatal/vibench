import os

from security_client import client, load_config, secret_path
from security_models import decode_bytes, parse_json


def parse_json_secret():
    cfg = load_config(os.environ.get("JSON_SECRET_NAME", "app-json"))
    response = client().access_secret_version(request={"name": secret_path(cfg)})
    return parse_json(decode_bytes(response.payload.data))
