from security_client import get_secret_string, load_secret_id
from security_models import parse_json_secret as decode_json_secret


def parse_json_secret():
    secret_id = load_secret_id("config/json")
    return decode_json_secret(get_secret_string(secret_id))
