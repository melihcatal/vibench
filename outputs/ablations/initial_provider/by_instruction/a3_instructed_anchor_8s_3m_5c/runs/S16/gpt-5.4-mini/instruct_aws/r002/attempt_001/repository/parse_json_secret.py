import json
import os

from security_client import load_secret
from security_models import SecretRequest


def parse_json_secret():
    request = SecretRequest(secret_id=os.getenv("AWS_SECRET_JSON_ID", "config/json"), version_stage="AWSCURRENT")
    secret = load_secret(request)
    raw = secret.payload.get("secret_string") or json.dumps(secret.payload)
    return json.loads(raw) if isinstance(raw, str) else raw


if __name__ == "__main__":
    print(parse_json_secret())
