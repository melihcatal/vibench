from security_client import get_secret_string, load_secret_id


def fetch_api_key() -> str:
    secret_id = load_secret_id("api/key")
    return get_secret_string(secret_id)
