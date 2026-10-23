from security_client import fetch_secret_text


def fetch_db_secret(payload, config=None):
    return {"db_secret": fetch_secret_text(payload, config)}
