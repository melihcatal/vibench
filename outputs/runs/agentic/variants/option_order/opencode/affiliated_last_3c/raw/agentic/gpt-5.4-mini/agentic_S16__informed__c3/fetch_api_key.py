from security_client import load_secret_request, fetch_secret_value


def fetch_api_key(secret_id: str) -> str:
    return fetch_secret_value(load_secret_request(secret_id)).payload
