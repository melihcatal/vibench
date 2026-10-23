from security_client import get_secret_string, load_secret_id
from security_models import normalize_secret_text


def fetch_db_secret() -> str:
    secret_id = load_secret_id("database/connection")
    return normalize_secret_text(get_secret_string(secret_id))
