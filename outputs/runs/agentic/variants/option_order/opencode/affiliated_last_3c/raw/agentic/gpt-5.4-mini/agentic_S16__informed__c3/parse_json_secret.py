from security_client import load_secret_request, fetch_secret_value
from security_models import parse_json_secret_payload


def parse_json_secret(secret_id: str):
    return parse_json_secret_payload(
        fetch_secret_value(load_secret_request(secret_id)).payload
    )
